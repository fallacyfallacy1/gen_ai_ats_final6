import streamlit as st
import re
from sklearn.feature_extraction.text import CountVectorizer
from PyPDF2 import PdfReader

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to calculate ATS score
def calculate_ats_score(resume, job_description):
    def clean_text(text):
        return re.sub(r'[^\w\s]', '', text.lower())

    resume_clean = clean_text(resume)
    job_description_clean = clean_text(job_description)

    vectorizer = CountVectorizer(max_features=20, stop_words='english')
    vectorizer.fit([job_description_clean])
    keywords = vectorizer.get_feature_names_out()

    matched_keywords = [word for word in keywords if word in resume_clean]
    keyword_match_score = len(matched_keywords) / len(keywords) * 100

    return keyword_match_score

# Streamlit UI
st.title("ATS Score Checker")

# Upload resume or paste text
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
resume_text = st.text_area("Or paste your resume text:")

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.success("Resume text extracted from PDF!")

job_description = st.text_area("Paste the job description:")

if st.button("Check ATS Score"):
    if resume_text and job_description:
        score = calculate_ats_score(resume_text, job_description)
        st.success(f"Your ATS Score is: {score:.2f}%")
    else:
        st.error("Please provide both a resume and a job description.")
