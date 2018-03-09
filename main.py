from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import pbkdf2_sha512
from database_setup import Base, UserAccount, Engine
from form import SignupForm


Base.metadata.create_all(Engine)
DBsession = sessionmaker(bind=Engine)
session = DBsession()


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5434/toxic'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    return session.query(UserAccount).filter_by(email = email).first()


@app.route('/')
def index():
    return "Welcome to Flask"


@app.route('/signup', methods=['GET', 'POST'])
def register():
    signupForm = SignupForm()

    if request.method == 'GET':
        return render_template('register.html', form = signupForm)
    elif request.method == 'POST':
        if signupForm.validate_on_submit():
            if session.query(UserAccount).filter_by(email=signupForm.email.data).first() is not None:
                return "Email address already exists"
            else:
                def encode_password(password):
                    return pbkdf2_sha512.hash(password)

                newuser = UserAccount(
                    email=signupForm.email.data,
                    password=encode_password(signupForm.password.data)
                )
                session.add(newuser)
                session.commit()
                login_user(newuser)

                return "User created!!!"
        else:
            return "Form didn't validate"


@app.route('/login', methods=['GET','POST'])
def login():
    loginForm = SignupForm()

    if request.method == 'GET':
        return render_template('login.html', form=loginForm)
    elif request.method == 'POST':
        if loginForm.validate_on_submit():
            user=session.query(UserAccount).filter_by(email=loginForm.email.data).first()
            if user is not None:
                if user.decode_password(loginForm.password.data):
                    login_user(user)
                    return "User logged in"
                else:
                    return "Wrong password"
            else:
                return "user doesn't exist"
        else:
            return "form not validated"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"


@app.route('/protected')
@login_required
def protected():
    return "protected area"


@app.route('/dashboard')
@login_required
def dashboard():
    return 'You are allowed to be here'


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True, use_reloader=True)