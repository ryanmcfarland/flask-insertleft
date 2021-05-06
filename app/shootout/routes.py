from datetime import datetime
from flask import request, render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Sheet, Weapon
from app.shootout import bp
from app.shootout.forms import SheetForm

# https://stackoverflow.com/questions/29451208/set-default-value-for-select-html-element-in-jinja-template

@bp.route('', methods=['GET','POST'])
@login_required
def so_home():
    page = request.args.get('page', 1, type=int)
    sheets = Sheet.query.filter_by(user_id=current_user.id).all()
    player_sheets = Sheet.query.filter(Sheet.user_id != current_user.id).paginate(page,9,False)
    next_url = url_for('shootout.so_home', page=player_sheets.next_num) if player_sheets.has_next else None
    prev_url = url_for('shootout.so_home', page=player_sheets.prev_num) if player_sheets.has_prev else None
    return render_template('shootout/shootout.html', sheets=sheets, player_sheets=player_sheets.items, next_url=next_url, prev_url=prev_url)

@bp.route('/sheet/<int:id>', methods=['GET'])
@login_required
def so_show(id):
    sheet = Sheet.query.get_or_404(id)
    sheet.update_bonuses()
    weapons = sheet.appended_weapons()
    sheet.output_md()    
    return render_template('shootout/sheet.html', sheet=sheet, weapons=weapons)

## process form from sheet, get specific row from sheet and update variables based on form data and commit
## will also check if data for weapon relationship per sheet needs to be updated / deleted
## will not save data if not validated
@bp.route('/sheet/edit/<int:id>', methods=['GET','POST'])
@login_required
def so_edit(id):
    sheet = Sheet.query.get_or_404(id)
    sheet.update_bonuses()
    weapons = sheet.appended_weapons()
    form = SheetForm(request.form)
    
    if request.method == "POST":
        if not form.validate():
            flash('Sheet was not updated, please check inputs', 'warning')
            return redirect(url_for('shootout.so_edit', id = id))       
        sheet.process_form(form)
        sheet.remove_form_weapons(request.form)
        sheet.last_update = datetime.utcnow()
        db.session.add(sheet)
        db.session.commit()
        flash('Sheet has been successfully updated', 'info')
        return redirect(url_for('shootout.so_show', id = id))
    return render_template('shootout/edit.html', sheet=sheet, weapons=weapons)

# This is not efficient -> selects table and then counts
# https://stackoverflow.com/questions/34692571/how-to-use-count-in-flask-sqlalchemy/35097740
@bp.route('/create', methods=['GET'])
@login_required
def so_create():
    count_sheets = Sheet.query.filter_by(user_id=current_user.id).count()
    if count_sheets < current_app.config['SHEETS_PER_USER']:
        sheet = Sheet(author=current_user)
        db.session.add(sheet)
        db.session.commit()
    else:
        flash(('Sheet limit: Cannot create more than '+str(current_app.config['SHEETS_PER_USER'])), 'Warning')
    return redirect(url_for('shootout.so_home'))

@bp.route('/sheet/delete/<int:id>', methods=['GET','POST'])
@login_required
def so_delete(id):
    sheet = Sheet.query.get_or_404(id)
    try:
        db.session.delete(sheet)
        db.session.commit()
    except:
        flash("Could not delete sheet", 'error')
    return redirect('/shootout')

@bp.route('/weapons', methods=['GET','POST'])
@bp.route('/weapons/sheet/<int:id>', methods=['GET','POST'])
@login_required
def weapon_sheet(id=None):
    if request.method == "POST":
        sheet = Sheet.query.get_or_404(id)
        sheet.append_form_weapons(request.form)
        db.session.commit()
        return redirect(url_for('shootout.so_edit', id = id))
    else:
        if id == None:
            add=False
            weapons = Weapon.query.all()
        else:
            add=True
            sheet = Sheet.query.get_or_404(id)
            weapons = sheet.missing_weapons()
        
        return render_template('shootout/weapons.html', id = id, weapons=weapons, add=add)