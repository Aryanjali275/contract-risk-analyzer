import streamlit as st
import pdfplumber

st.title("📂 Upload Contract")

uploaded_file = st.file_uploader("Upload a contract", type=["pdf", "txt"])

if uploaded_file:
    text = ""

    # PDF handling
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        text = uploaded_file.read().decode("utf-8", errors="ignore")

    # Store text
    st.session_state["contract_text"] = text

    st.success("File uploaded and processed successfully!")

    st.text_area("Preview", text[:1000], height=300)