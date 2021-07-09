import datetime
import requests

from flask import current_app
from flask_mail import Message
from app import db, mail
from app.models import Role, User
from app.common import bp

# Run this function whenever flask starts and the first request is sent
# ensures required roles are seeded in the db alongside the admin user I want
@bp.before_app_first_request
def startup_functions():
    add_roles_on_startup()
    create_admin_on_startup()
    assign_admin_to_admin()

# Create User Role if not already part of the database
def add_roles_on_startup():
    for i in ["Admin", "Power", "User"]:
        i=i.capitalize()
        r = Role.query.filter_by(name=i).first()
        if not r:
            r = Role(name=i)
            try:
                db.session.add(r)
                db.session.commit()
            except:
                db.session.rollback()
                print("Error - rollbacking the db")
            print("Added Role: "+i)
        else:
            print("Role added already: "+i)

# create admin user at start-up if it does not exist and send to my main email address
def create_admin_on_startup(username="ryanmcfarland", email="insertleft@outlook.com"):
    u = User.query.filter_by(username=username).first()
    if not u:
        u = User(username=username, email=email)
        password=generate_temp_password(12)
        u.set_password(password)
        u.verified=True
        try:
            db.session.add(u)
            db.session.commit()
            subject=(datetime.date.today().strftime("%Y.%m.%d"))+" - Flask Admin Password"
            send_email(subject, sender=current_app.config["ADMIN"], recipients=[email], text_body=password, html_body=password)
        except:
            db.session.rollback()
            print("Error - rollbacking the db")
        print("Added User: "+username)
    else:
        print("User added already: "+username)

# Append whatever roles I need to the admin user
def assign_admin_to_admin(username="ryanmcfarland"):
    u = User.query.filter_by(username=username).first()
    u.append_role("Admin")
    db.session.commit()

# Taken from: https://stackoverflow.com/questions/3854692/generate-password-in-python
def generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    from os import urandom

    # Python 3 (urandom returns bytes)
    return "".join(chars[c % len(chars)] for c in urandom(length))


# Wrapper to send mail via flask_mail
def send_email(subject, sender, recipients, text_body, html_body=None, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    #msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    mail.send(msg)

def verify_recaptcha(response):
    data = {
                "secret": current_app.config['RECAPTCHA_SECRET_KEY'],
                "response": response
            }
    r = requests.get(current_app.config['RECAPTCHA_SITE_VERIFY'], params=data)
    return r.json()["success"] if r.status_code == 200 else False