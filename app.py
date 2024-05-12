import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from bs4 import BeautifulSoup
import requests
from PyPDF2 import PdfReader

# Load pretrained summarization model (Flan-T5)
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Summarize content using Flan-T5
def summarize_text(text, max_length=100):
    try:
        # Generate a summary using the model
        summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
        return summary[0]['generated_text']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Extract text from PDF
def extract_text_from_pdf(file):
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

# Evaluate a project proposal
def evaluate_proposal(proposal):
    scoring_criteria = {
        "Innovation": 0.4,
        "Feasibility": 0.3,
        "Impact": 0.2,
        "Alignment with Trends": 0.1
    }
    score = 0
    for criterion, weight in scoring_criteria.items():
        if criterion.lower() in proposal.lower():
            score += 10 * weight  # Simulated score
    return round(score, 2)

# Streamlit UI
st.title("AI Tool for Summarization, Proposal Evaluation, and Web Research")
st.sidebar.title("Options")

option = st.sidebar.selectbox(
    "Choose a feature:",
    ["Summarize Text", "Summarize File (PDF)", "Evaluate Proposal", "Evaluate PDF Proposal", "Find Academic Papers", "Find Patents"]
)

if option == "Summarize Text":
    st.header("Summarize Text")
    text = st.text_area("Enter text to summarize:")
    max_length = st.slider("Max summary length:", 50, 200, 100)
    if st.button("Summarize"):
        summary = summarize_text(text, max_length)
        st.subheader("Summary")
        st.write(summary)

elif option == "Summarize File (PDF)":
    st.header("Summarize File")
    uploaded_file = st.file_uploader("Upload a PDF file:", type=["pdf"])
    max_length = st.slider("Max summary length:", 50, 200, 100)
    if uploaded_file and st.button("Summarize PDF"):
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text.startswith("Error"):
            st.error(pdf_text)
        else:
            summary = summarize_text(pdf_text, max_length)
            st.subheader("Summary")
            st.write(summary)

elif option == "Evaluate Proposal":
    st.header("Evaluate Project Proposal")
    proposal = st.text_area("Enter your project proposal:")
    if st.button("Evaluate"):
        score = evaluate_proposal(proposal)
        st.subheader("Proposal Score")
        st.write(f"Your proposal scored: {score}/10")

elif option == "Evaluate PDF Proposal":
    st.header("Evaluate Project Proposal from PDF")
    uploaded_file = st.file_uploader("Upload a PDF file containing your proposal:", type=["pdf"])
    if uploaded_file and st.button("Evaluate PDF Proposal"):
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text.startswith("Error"):
            st.error(pdf_text)
        else:
            score = evaluate_proposal(pdf_text)
            st.subheader("Proposal Score")
            st.write(f"Your proposal scored: {score}/10")

elif option == "Find Academic Papers":
    st.header("Find Academic Papers")
    topic = st.text_input("Enter topic to search for academic papers:")
    if st.button("Search Papers"):
        papers = find_academic_papers(topic)
        st.subheader("Academic Papers")
        for paper in papers:
            st.write(f"**Title:** {paper['title']}")
            st.write(f"**Link:** [Read More]({paper['link']})")
            st.write(f"**Snippet:** {paper['snippet']}")
            st.write("---")

elif option == "Find Patents":
    st.header("Find Patents")
    keyword = st.text_input("Enter keyword to search for patents:")
    if st.button("Search Patents"):
        patents = find_patents(keyword)
        st.subheader("Patents")
        for patent in patents:
            st.write(f"**Title:** {patent['title']}")
            st.write(f"**Link:** [Read More]({patent['link']})")
            st.write("---")
