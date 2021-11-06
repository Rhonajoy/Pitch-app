from . import auth
from flask import render_template,redirect,url_for
from ..models import User
from .forms import RegistrationForm
from .. import db


@auth.route('/login')
def login():
    return render_template('auth/login.html')
@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name = form.first_name.data,last_name = form.last_name.data,email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)