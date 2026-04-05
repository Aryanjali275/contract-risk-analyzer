import streamlit as st

st.title("Analysis Result")

text = st.session_state.get("contract_text", "")

if text:
    text_lower = text.lower()
    risks = []

    # Risk detection
    if "penalty" in text_lower:
        risks.append("Penalty clause detected")
    if "terminate" in text_lower:
        risks.append("Termination clause detected")
    if "liability" in text_lower:
        risks.append("Liability clause detected")
    if "breach" in text_lower:
        risks.append("Breach condition detected")

    # Risk scoring
    if len(risks) >= 3:
        risk_level = "High"
        score = 80
    elif len(risks) == 2:
        risk_level = "Medium"
        score = 50
    elif len(risks) == 1:
        risk_level = "Low"
        score = 30
    else:
        risk_level = "Very Low"
        score = 10

    # Layout with columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Level")
        if risk_level == "High":
            st.error("High Risk")
        elif risk_level == "Medium":
            st.warning("Medium Risk")
        else:
            st.success("Low Risk")

    with col2:
        st.subheader("Risk Score")
        st.metric(label="Score", value=score)

    st.subheader("Detected Risks")

    if risks:
        for r in risks:
            st.markdown(f"- {r}")
    else:
        st.success("No major risks detected")

    st.subheader("Contract Preview")
    st.text_area("", text[:1000], height=300)

else:
    st.warning("Please upload a contract first.")