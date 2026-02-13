from flask import Flask, render_template, request, session
import pickle
import pandas as pd
from urllib.parse import urlparse
from feature_extraction import extract_features

app = Flask(__name__)
app.secret_key = "phishing_detector_secret_key_2026"

# ---------------- Load Model ----------------
with open("model.pkl", "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
model_columns = saved["columns"]

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        url = request.form["url"].strip().lower()

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        features_dict = extract_features(url)

        feature_df = pd.DataFrame([features_dict])
        feature_df = feature_df[model_columns]

        # ---------------- Rule-Based Quick Filter ----------------
        domain = urlparse(url).netloc

        rule_flag = (
            "@" in url or
            domain.count("-") >= 3 or
            domain.replace(".", "").isdigit() or
            any(short in domain for short in ["bit.ly", "tinyurl", "goo.gl"])
        )

        if rule_flag:
            prediction = "Phishing Website"
            confidence = 100.0
        else:
            result = model.predict(feature_df)[0]
            prob = model.predict_proba(feature_df)[0]
            confidence = round(max(prob) * 100, 2)

            prediction = "Legitimate Website" if result == 1 else "Phishing Website"

        session["history"].append((url, prediction))
        session.modified = True

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        history=session["history"][::-1]
    )

if __name__ == "__main__":
    app.run(debug=True)
