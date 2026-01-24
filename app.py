from flask import Flask, render_template, request
import pickle
from urllib.parse import urlparse
from feature_extraction import extract_features

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Store history
history = []

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        url = request.form["url"].lower()
        features = extract_features(url)

        # Extract DOMAIN only
        domain = urlparse(url).netloc

        # If user enters without https://
        if domain == "":
            domain = urlparse("http://" + url).netloc

        # RULE-BASED CHECK
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
            result = model.predict([features])[0]
            prediction = "Legitimate Website" if result == 1 else "Phishing Website"

        # Save to history
        history.append((url, prediction))

    return render_template(
        "index.html",
        prediction=prediction,
        history=history[::-1]  # latest first
    )

if __name__ == "__main__":
    app.run(debug=True)
