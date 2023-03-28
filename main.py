from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import os
from models import db, login_manager, User

app = Flask(__name__)
db_url = os.environ.get('DB_URL')
DATABASE_URL = db_url.replace(
    'postgres://',
    'postgresql://',
    1
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
app.app_context().push()
db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            flash('User already exists. Please login')
            return redirect(url_for('login'))
        new_user = User(
        name = request.form['name'],
        email = request.form['email'],
        password = generate_password_hash(request.form['password'],method='pbkdf2:sha256',salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('secrets'))

    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('secrets'))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    user_name = current_user.name
    logged_in = current_user.is_authenticated
    return render_template("secrets.html", name=user_name,logged_in=logged_in )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/download')
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf',as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
