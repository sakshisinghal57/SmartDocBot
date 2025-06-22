
import streamlit as st
import PyPDF2
from openai import AzureOpenAI

# Azure OpenAI Setup
client = AzureOpenAI(
    api_key="8WxLaoodYxa7XSK2rCiWuP3nqwWUShSUVd5FrjEYSqqROfIwc0qzJQQJ99BFAC77bzfXJ3w3AAABACOGweqQ",
    azure_endpoint="https://mindcraft-kapidhwaj-openai-api-key.openai.azure.com/",
    api_version="2024-12-01-preview"
)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to summarize text using Azure OpenAI
def get_summary(text):
    prompt = f"Summarize the following text:\n\n{text}"
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Function to answer user question using Azure OpenAI
def ask_question(text, question):
    prompt = f"The following is a document:\n{text}\n\nQuestion: {question}\nAnswer:"
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Optional: Quiz Generator (bonus)
def generate_quiz(text):
    prompt = f"Based on this text, create 3 multiple choice questions with 4 options each. Mark the correct answer clearly:\n\n{text}"
    response = client.chat.completions.create(
        model="mindcraft-gpt4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("📚 DocuSage: The AI PDF Whisperer")
st.markdown("""<small><i>by Sakshi Singhal | Powered by Azure OpenAI</i></small>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("📋 Document Summary")
    if st.button("Generate Summary"):
        with st.spinner("Generating summary..."):
            summary = get_summary(text[:3000])
            st.success("Summary generated!")
            st.write(summary)

    st.subheader("💬 Ask a Question")
    user_question = st.text_input("Enter your question based on the document")
    if st.button("Get Answer"):
        with st.spinner("Answering your question..."):
            answer = ask_question(text[:3000], user_question)
            st.success("Answer generated!")
            st.write("🤖 Answer:", answer)

    st.subheader("📝 Auto-Quiz Generator")
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(text[:5000])
            st.success("Quiz ready!")
            st.write(quiz)