import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Function to configure Google API
def configure_google_api():
    load_dotenv()
    if os.getenv("GOOGLE_API_KEY") is None:
        st.error("Please configure the Google API key.")
        st.stop()

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Configure Google API
configure_google_api()

# Streamlit app
st.title("Smart ATS - Resume Improvement Assistant")
st.write("Evaluate your resume against a job description to improve it.")

jd = st.text_area("Paste the Job Description Here:")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload your resume in PDF format.")

submit = st.button("Submit")

if submit:
    st.text("Processing... Please wait.")
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        text = input_pdf_text(uploaded_file)

        # Define input prompt
        input_prompt = f"""
        Hey Act Like a skilled or very experienced ATS (Application Tracking System)
        with a deep understanding of tech field, software engineering, data science, data analyst,
        and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive, and you should provide 
        the best assistance for improving the resumes. Assign the percentage Matching based 
        on JD and the missing keywords with high accuracy.
        resume: {text}
        description: {jd}

        I want the response in one single string having the structure
        {{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
        """

        # Get response from Gemini model
        response = get_gemini_response(input_prompt)

        # Display result
        st.subheader("Result:")
        st.json(response)
    else:
        st.error("Please upload a resume before submitting.")
