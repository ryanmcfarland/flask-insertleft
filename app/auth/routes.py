from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


# - using wtforms to only validate my incoming form data - data checks aere handled in the route
# - uses next inbuilt arg to redirect the user back to original page they had originally requested 
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'error')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            page = request.args.get('next', url_for('main.index'), type=str)
            return redirect(page)
    else:
        return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# - Uses wtfforms validators to get error message and check the form inputs
# - Will not validate form if field is not validated and thus user will not be registered
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        form = RegistrationForm(request.form)
        if form.validate():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                flash('Database error, please try again', 'error')
                return redirect(url_for('auth.register'))               
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login'))
        elif "username" in form.errors:
            flash(form.errors['username'][0], 'warn')
        elif "email" in form.errors:
            flash(form.errors['email'][0], 'warn')
        elif "password2" in form.errors:
            flash(form.errors['password2'][0], 'warn')
        else:
            flash('Form data could not be processed, please try again', 'warn')
        return redirect(url_for('auth.register'))

