import streamlit as st
import PyPDF2

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("📄 Contract Risk Analyzer")

page = st.sidebar.radio("Navigate", ["Home", "Analyzer", "About"])

# ------------------ FUNCTIONS ------------------

def extract_text(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def analyze_risk(text):
    risks = []

    high_risk_keywords = ["penalty", "termination", "liability", "breach"]
    medium_risk_keywords = ["delay", "payment", "obligation"]

    for word in high_risk_keywords:
        if word in text.lower():
            risks.append(("High", word))

    for word in medium_risk_keywords:
        if word in text.lower():
            risks.append(("Medium", word))

    if not risks:
        risks.append(("Low", "No major risks found"))

    return risks

# ------------------ HOME PAGE ------------------

if page == "Home":
    st.title("📑 AI Contract Risk Analyzer")
    st.write("Upload contracts and detect potential risks instantly.")

    st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f", use_container_width=True)

    st.markdown("""
    ### Features:
    - Upload PDF contracts
    - Detect risky clauses
    - Get instant insights
    """)

# ------------------ ANALYZER PAGE ------------------

elif page == "Analyzer":
    st.title("🔍 Contract Analyzer")

    uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])

    if uploaded_file:
        text = extract_text(uploaded_file)

        # Split layout (like Kira)
        col1, col2 = st.columns([2, 1])

        # LEFT → Contract Preview
        with col1:
            st.subheader("📄 Contract Preview")
            st.text_area("Text", text, height=500)

        # RIGHT → Risk Analysis
        with col2:
            st.subheader("⚠️ Risk Analysis")

            risks = analyze_risk(text)

            for level, word in risks:
                if level == "High":
                    st.error(f"🔴 High Risk: {word}")
                elif level == "Medium":
                    st.warning(f"🟡 Medium Risk: {word}")
                else:
                    st.success(f"🟢 {word}")

            st.markdown("---")
            st.subheader("📊 Summary")

            st.write(f"Total Risks Found: {len(risks)}")

# ------------------ ABOUT PAGE ------------------

elif page == "About":
    st.title("ℹ️ About")
    st.write("""
    This project analyzes contracts and identifies potential risks using basic NLP techniques.

    Built using:
    - Python
    - Streamlit
    - PyPDF2
    """)