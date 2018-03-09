from flask import Flask
from flask import render_template, request, url_for, redirect, flash, session, sessions

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import pbkdf2_sha512
from functools import wraps

from database_setup import Base, UserAccount, Engine


Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

app = Flask(__name__)
app.secret_key = 'xxx'


def check_user(user):
    return session.query(UserAccount).filter_by(
        name=user
    ).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userExists = check_user(request.form['username'])
        if userExists is not None:
            if userExists.decode_password(request.form['password']):
                return redirect(url_for('dashboard', user_id=userExists.id))
        else:
            return redirect(url_for('register'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userExists = check_user(request.form['username'])
        if userExists is not None:
            return redirect(url_for('login'))
        else:
            def encode_password(password):
                return pbkdf2_sha512.hash(password)
            user = UserAccount(
                name=request.form['username'],
                password=encode_password(request.form['password'])
            )
            session.add(user)
            session.commit()
            return redirect(url_for('dashboard', user_id=user.id))
    else:
        return render_template('register.html')


@app.route('/dashboard/<int:user_id>', methods=['GET'])
def dashboard(user_id):
    return 'you are home'


app.run(debug=True, use_reloader=True)