from flask import Flask, request, render_template
import pickle
import re

app = Flask(__name__)

tfidf = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
svm_model = pickle.load(open("svm_sentiment_model.pkl", "rb"))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = None
    review_text = ""

    if request.method == "POST":
        review_text = request.form["review"]

        cleaned = clean_text(review_text)
        vector = tfidf.transform([cleaned])
        prediction = svm_model.predict(vector)[0]

        sentiment = "Positive" if prediction == "positive" else "Negative"

    return render_template("index.html", sentiment=sentiment, review=review_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
