from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Grocery, User, Sheet
from app.main import bp

import logging

LOG = logging.getLogger(__name__)

#@bp.before_app_request
#def before_request():
#    if current_user.is_authenticated:
#        g.user = current_user.get_id() # return username in get_id()
#    else:
#        g.user = None # or 'some fake value', whatever

@bp.route('/', methods=['GET','POST'])
@bp.route('/index',  methods=['GET','POST'])
def index():
    user1 = {'username': 'Ryan'}
    return render_template('home.html', title="hello", user=user1)

# https://stackoverflow.com/questions/43634409/switch-chart-js-data-with-button-click

@bp.route('/shootout', methods=['GET','POST'])
@login_required
def shootout():
    user1 = {'username': 'Ryan'}
    return render_template('shootout_sheet.html', title="hello", user=user1)

@bp.route('/random', methods=['GET','POST'])
def random():
    user = {'username': 'Ryan'}
    if request.method == "POST":
        text = request.form['text']
        processed_text = text.upper()
        print(processed_text)
        text = request.form['text1']
        processed_text = text.upper()
        print(processed_text)
    return render_template('random.html', title="hello", user=user)

@bp.route('/shootout/<int:id>/', methods=['GET','POST'])
def sheet():
    if  request . method  ==  'POST' :
        name = request.form['name']
        LOG.debug(name)
        name3 = request.form['name3']
        LOG.debug(name3)
        #new_stuff = Grocery(name=name)

        try:
            #db.session.add(new_stuff)
            #db.session.commit()
            return redirect('/crud')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('crud.html', groceries=groceries) 



@bp.route('/crud', methods=['GET','POST'])
def crud():
    if  request . method  ==  'POST' :
        name = request.form['name']
        LOG.debug(name)
        name3 = request.form['name3']
        LOG.debug(name3)
        #new_stuff = Grocery(name=name)

        try:
            #db.session.add(new_stuff)
            #db.session.commit()
            return redirect('/crud')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('crud.html', groceries=groceries) 

    