from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import string, random, validators

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(9), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 5 or len(username) > 9:
            flash("Username must be between 5 to 9 characters")
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('signup'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Signup successful! Please login.")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    short_url = None

    if request.method == 'POST':
        long_url = request.form['url']

        if not validators.url(long_url):
            flash("Invalid URL")
            return redirect(url_for('dashboard'))

        existing_url = URL.query.filter_by(
            original_url=long_url,
            user_id=session['user_id']
        ).first()

        if existing_url:
            short_url = request.host_url + existing_url.short_code
            flash("URL already shortened. Showing existing short URL.")
        else:
            short_code = generate_short_code()
            new_url = URL(
                original_url=long_url,
                short_code=short_code,
                user_id=session['user_id']
            )
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + short_code

    urls = URL.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', short_url=short_url, urls=urls)


@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
