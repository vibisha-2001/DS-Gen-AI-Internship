from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import validators
import string
import random
app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        original_url = request.form.get("url")
        if not original_url:
            flash("Please enter a URL")
            return render_template("home.html")
        if not validators.url(original_url):
            flash("Invalid URL. Please enter a valid URL.")
            return render_template("home.html")
        
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            short_url = request.host_url + existing_url.short_code
            flash("This URL was already shortened. Showing existing short link.")
        else:
            short_code = generate_short_code()
            new_url = URL(original_url=original_url, short_code=short_code)
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + short_code

    return render_template("home.html", short_url=short_url)


@app.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if url:
        return redirect(url.original_url)
    else:
        return "URL not found", 404
    
@app.route("/history")
def history():
    urls = URL.query.all()
    return render_template("history.html", urls=urls)

if __name__ == "__main__":
    app.run(debug=True)

