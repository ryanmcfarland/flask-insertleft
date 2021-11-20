from app import db
from flask import request, render_template, flash, redirect, url_for, current_app
from flask.views import MethodView
from flask_login import current_user, login_required
from werkzeug.exceptions import Forbidden

# This can't be a decotor within a view due to the lack of ability to access self
# needs to be added to all required functions
def user_or_admin(Sheet, id):
    """
    Returns Forbidden or None.
    
    Checks if the user id is either an Admin or is the owner of the sheet.
    """
    if current_user.check_roles('Admin') or Sheet.query.filter_by(user_id=current_user.id).filter_by(id=id).all():
        return None
    else:
        return Forbidden("You do not have access")


class Home(MethodView):
    def __init__(self, Sheet, route):
        self.Sheet = Sheet
        self.route = route


    @login_required
    def get(self):
        sheets = self.Sheet.query.filter_by(user_id=current_user.id).all()
        return render_template('rpg/home.html', sheets=sheets)


class Show(MethodView):
    def __init__(self, Sheet, Config, route):
        self.Sheet = Sheet
        self.Config = Config
        self.route = route

    def get(self, id):
        sheet = self.Sheet.query.get_or_404(id)
        weapons = sheet.appended_weapons()
        sheet.output_md()    
        return render_template('rpg/sheet.html', sheet=sheet, config=self.Config, weapons=weapons) 


# This is not efficient -> selects table and then counts
# https://stackoverflow.com/questions/34692571/how-to-use-count-in-flask-sqlalchemy/35097740
class Create(MethodView):
    def __init__(self, Sheet, route):
        self.Sheet = Sheet
        self.route = route

    @login_required
    def post(self):
        count_sheets = self.Sheet.query.filter_by(user_id=current_user.id).count()
        if count_sheets < current_app.config['SHEETS_PER_USER'] or current_user.check_roles(["Admin", "Power"]):
            sheet = self.Sheet(author=current_user)
            sheet.save()
        else:
            flash(('Sheet limit: Cannot create more than '+str(current_app.config['SHEETS_PER_USER'])), 'Warning')
        return redirect(url_for(self.route+'.home'))

# TODO - ajax call?
class Delete(MethodView):
    def __init__(self, Sheet, route):
        self.Sheet = Sheet
        self.route = route

    decorators = [login_required]

    def get(self, id):
        sheet = self.Sheet.query.get_or_404(id)
        try:
            db.session.delete(sheet)
            db.session.commit()
        except:
            db.session.rollback()
            flash("Could not delete sheet", 'error')
        return redirect(url_for(self.route+'.home'))

    def post(self, id):
        sheet = self.Sheet.query.get_or_404(id)
        try:
            db.session.delete(sheet)
            db.session.commit()
        except:
            db.session.rollback()
            flash("Could not delete sheet", 'error')
        return redirect(url_for(self.route+'.home'))


## process form from sheet, get specific row from sheet and update variables based on form data and commit
## will also check if data for weapon relationship per sheet needs to be updated / deleted
## will not save data if not validated
#https://stackoverflow.com/questions/44119600/how-to-keep-input-after-failed-form-validation-in-flask
#https://stackoverflow.com/questions/43310740/how-to-set-up-an-inherited-methodview-in-flask-to-do-crud-operations-on-sqlalche
class Edit(MethodView):
    def __init__(self, Sheet, SheetForm, Config, route):
        self.Sheet = Sheet
        self.SheetForm = SheetForm
        self.Config = Config
        self.route = route

    decorators = [login_required]

    def get(self, id):
        access = user_or_admin(self.Sheet,id)
        if access is not None: return access
        form = self.SheetForm(request.form)
        sheet = self.Sheet.query.get_or_404(id)
        form.process(obj=sheet)
        weapons = sheet.appended_weapons()
        return render_template('rpg/edit.html', sheet=form, weapons=weapons, config=self.Config, id = id)

    def post(self, id):
        access = user_or_admin(self.Sheet,id)
        if access is not None: return access
        form = self.SheetForm(request.form)
        sheet = self.Sheet.query.get_or_404(id)
        weapons = sheet.appended_weapons()
        if not form.validate():
            flash('Sheet cannot be updated, please check inputs: '+" ,".join([*form.errors]), 'error')
            return render_template('rpg/edit.html', sheet=form, weapons=weapons, config=self.Config, id = id)
        sheet.remove_form_weapons(request.form)
        if sheet.process_and_save(form):
            flash('Sheet has been successfully updated', 'info')
            return redirect(url_for(self.route+'.show', id = id))
        else:
            flash('Sheet cannot be updated, database error', 'error')
            return redirect(url_for(self.route+'.edit', id = id))


class Weapon(MethodView):
    def __init__(self, Sheet, route, Weapon):
        self.Sheet = Sheet
        self.Weapon = Weapon
        self.route = route

    @login_required
    def get(self, id = None):
        if id == None:
            add=False
            weapons = Weapon.query.all()
        else:
            add=True
            sheet = self.Sheet.query.get_or_404(id)
            weapons = sheet.missing_weapons()
        return render_template('rpg/weapons.html', id = id, weapons=weapons, add=add)
    
    @login_required
    def post(self, id):
        sheet = self.Sheet.query.get_or_404(id)
        sheet.append_form_weapons(request.form)
        db.session.commit()
        return redirect(url_for(self.route+'.edit', id = id))


def register_urls(bp, Sheet, SheetForm, Weapons, Config):
    home = Home.as_view('home', Sheet, bp.name)
    show = Show.as_view('show', Sheet, Config, bp.name)
    create = Create.as_view('create', Sheet, bp.name)
    delete = Delete.as_view('delete', Sheet, bp.name)
    edit = Edit.as_view('edit', Sheet, SheetForm, Config, bp.name)
    weapon = Weapon.as_view('weapons', Sheet, Weapons, bp.name)

    bp.add_url_rule('/home', view_func=home)
    bp.add_url_rule('/sheet/<int:id>', view_func=show)
    bp.add_url_rule('/create', view_func=create)
    bp.add_url_rule('/delete/<int:id>', view_func=delete)
    bp.add_url_rule('/edit/<int:id>', view_func=edit)
    bp.add_url_rule('/weapons', view_func=weapon)
    bp.add_url_rule('/weapons/sheet/<int:id>', view_func=weapon)