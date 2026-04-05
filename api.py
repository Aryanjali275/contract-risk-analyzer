from flask import Flask, request, jsonify
import pdfplumber
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/analyze", methods=["POST"])
def analyze_contract():
    file = request.files["file"]

    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    risk_dict = {
        "HIGH": ["unlimited liability", "indemnity", "breach"],
        "MEDIUM": ["termination", "penalty"],
        "LOW": ["liability"]
    }

    doc = nlp(text)
    risky_sentences = []

    for sent in doc.sents:
        sentence_text = sent.text.lower()
        for level, words in risk_dict.items():
            for word in words:
                if word in sentence_text:
                    risky_sentences.append({
                        "sentence": sent.text,
                        "risk": level
                    })
                    break

    return jsonify({
        "risks": risky_sentences
    })

if __name__ == "__main__":
    app.run(debug=True)