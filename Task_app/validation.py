
from flask import Blueprint , render_template,redirect,url_for,request,flash
from . import db
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash


validation = Blueprint('validation',__name__)


@validation.route("/signup", methods = ["GET","POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username= request.form.get("username")
        password1 = request.form.get("password1")
        passwodr2 = request.form.get("password2")
        contact = request.form.get("contact")
        
        email_exists=User.query.filter_by(email=email).first()
        user_exists=User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already exist',category='error')
        elif user_exists:
            flash('User already exixts',category='error')
        elif password1!= passwodr2:
            flash('Password does not match',category='error')
        elif len(username)<2:
            flash('Username is too short',category='error')
        elif len(password1)<8:
            flash('Password is too short',category='error')
        elif len(email)<10:
            flash('Invalid Email',category='error')
        elif len(contact)<10:
            flash('Invalid Contact',category='error')
        else:
            new_user = User(email = email,username = username,password =generate_password_hash(password1,method = 'sha256'),contact = contact)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember = True)
            flash('User created')

            return redirect(url_for('show.index'))
    return render_template('signup.html', user = current_user)

@validation.route("/login",methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password ,password):
                flash('Logged in',category='success')
                login_user(user,remember = True)
                return redirect(url_for('show.index'))
            else:
                flash('Password is incorrect',category = 'error')
        else:
            flash('Email does not exist',category = 'error')
    return render_template('login.html',user = current_user)





@validation.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("show.index"))

