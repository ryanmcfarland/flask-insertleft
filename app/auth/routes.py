from flask import render_template, redirect, url_for, flash, request
from flask.globals import current_app
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.common.utils import verify_recaptcha 


# - using wtforms to only validate my incoming form data - data checks aere handled in the route
# - uses next inbuilt arg to redirect the user back to original page they had originally requested 
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter((User.lowercase_username==form.login.data.lower()) | (User.email==form.login.data)).first()
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
    if request.method == 'POST':
        form = RegistrationForm(request.form)
        recapthca = verify_recaptcha(request.form['g-recaptcha-response'])
        if form.validate() and recapthca:
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
            flash("Username Field - "+form.errors['username'][0], 'warn')
        elif "email" in form.errors:
            flash("Email Field - "+form.errors['email'][0], 'warn')
        elif "password2" in form.errors:
            flash(form.errors['password2'][0], 'warn')
        elif not recapthca:
            flash("Recaptcha could not be verified", 'warn')
        else:
            flash('Form data could not be processed, please try again', 'warn')
    return render_template('auth/register.html')
