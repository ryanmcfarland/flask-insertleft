from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Grocery, User, Sheet, Weapon
from app.main import bp
from app.main.forms import SheetForm, WeaponForm

import logging

LOG = logging.getLogger(__name__)

## TODO https://www.askpython.com/python-modules/flask/flask-redirect-url

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


## process form from sheet, get specific row from sheet and update variables based on form data and commit
## will also check if data for weapon relationship per sheet needs to be updated / deleted
## will not save data if not validated
@bp.route('/shootout/sheet/<int:id>', methods=['GET','POST'])
@login_required
def shootout_edit(id):
    form = SheetForm(request.form)
    if request.method == "POST":
        sheet = db.session.query(Sheet).get(id)
        if form.validate() and form.submit.data == "save":
            sheet.process_form(form)
        elif "delete" in request.form:
            sheet.remove_form_weapons(request.form)
        else:
            flash('Sheet was not updated, please check inputs', 'warning')
            sheet.update_bonuses()
            weapons = sheet.appended_weapons()
            return render_template('shootout_sheet.html', title="Shootout - Sheet", sheet=sheet, weapons=weapons)
        
        sheet.update_bonuses()
        sheet.last_update = datetime.utcnow()
        db.session.add(sheet)
        db.session.commit()
        flash('Sheet has been successfully updated', 'info')

    sheet = Sheet.query.get_or_404(id)
    sheet.update_bonuses()
    weapons = sheet.appended_weapons()
    return render_template('shootout_sheet.html', title="Shootout - Sheet", sheet=sheet, weapons=weapons)

@bp.route('/shootout/create', methods=['GET'])
@login_required
def shootout_create():
    sheet = Sheet(author=current_user)
    db.session.add(sheet)
    db.session.commit()
    return redirect(url_for('main.shootout'))

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

@bp.route('/shootout/weapons', methods=['GET','POST'])
@bp.route('/shootout/weapons/sheet/<int:id>', methods=['GET','POST'])
@login_required
def weapon_sheet(id=None, add=1):
    if request.method == "POST":
        sheet = Sheet.query.get_or_404(id)
        sheet.append_form_weapons(request.form)
        db.session.commit()
        return redirect(url_for('main.shootout_edit', id = id))
    else:
        if id == None:
            weapons = Weapon.query.all()
        else:
            sheet = Sheet.query.get_or_404(id)
            weapons = sheet.missing_weapons()
    return render_template('shootout_weapons.html', title="Shootout - Weapons", id = id, weapons=weapons, add=add)

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

    