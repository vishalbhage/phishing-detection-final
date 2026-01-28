from flask import Flask, render_template, request, session
import pickle
import pandas as pd
from urllib.parse import urlparse
from feature_extraction import extract_features

app = Flask(__name__)
app.secret_key = "phishing_detector_secret_key_2026"  # required for sessions

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    # Create separate history for each user
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        url = request.form["url"].lower()
        features = extract_features(url)

        # Extract DOMAIN only
        domain = urlparse(url).netloc
        if domain == "":
            domain = urlparse("http://" + url).netloc

        # ---------------- Rule-Based Quick Check ----------------
        if (
            "@" in url or
            domain.count("-") >= 3 or
            domain.replace(".", "").isdigit() or
            "bit.ly" in domain or
            "tinyurl" in domain or
            ("secure" in domain and "login" in domain)
        ):
            prediction = "Phishing Website"
        else:
            # ---------------- ML Prediction ----------------
            feature_df = pd.DataFrame([features], columns=model.feature_names_in_)
            result = model.predict(feature_df)[0]
            prediction = "Legitimate Website" if result == 1 else "Phishing Website"

        # Save per-user history
        session["history"].append((url, prediction))
        session.modified = True

    return render_template(
        "index.html",
        prediction=prediction,
        history=session["history"][::-1]  # latest first
    )

if __name__ == "__main__":
    app.run(debug=True)
