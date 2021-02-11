from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Grocery, User, Sheet
from app.main import bp
from app.main.forms import SheetForm


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
    sheets = Sheet.query.filter_by(user_id=current_user.id).all()
    return render_template('shootout.html', title="Shootout", sheets=sheets)

## process form from sheet, get specific row from sheet 
## and update variabels based on form data and commit
## will not save data if not validated
@bp.route('/shootout/sheet/<int:id>', methods=['GET','POST'])
@login_required
def shootout_edit(id):
    form = SheetForm(request.form)
    if request.method == "POST" and form.validate():
        sheet = db.session.query(Sheet).get(id)
        sheet.process_form(form)
        db.session.add(sheet)
        db.session.commit()
        flash('DB has been successfully updated')
        return redirect(url_for('main.shootout'))
    sheet = Sheet.query.get_or_404(id)
    return render_template('shootout_sheet.html', title="Shootout - Sheet", sheet=sheet)

@bp.route('/shootout/delete/<int:id>', methods=['GET','POST'])
@login_required
def shootout_delete(id):
    sheet = Sheet.query.get_or_404(id)
    try:
        db.session.delete(sheet)
        db.session.commit()
        return redirect('/shootout')
    except:
        return "Problem with deleting data - please try again"
    return redirect('/shootout')

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

    