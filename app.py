from flask import Flask, render_template, request
import pickle
from urllib.parse import urlparse
from feature_extraction import extract_features

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        url = request.form["url"].lower()
        features = extract_features(url)

        # Extract DOMAIN only
        domain = urlparse(url).netloc

        # ✅ IMPROVED RULE-BASED CHECK (DOMAIN-BASED)
        if (
            "@" in url or
            domain.count("-") >= 3 or
            domain.replace(".", "").isdigit() or   # IP-like domain
            "bit.ly" in domain or
            "tinyurl" in domain or
            ("secure" in domain and "login" in domain)
        ):
            prediction = "Phishing Website"
        else:
            result = model.predict([features])[0]
            prediction = "Legitimate Website" if result == 1 else "Phishing Website"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)

