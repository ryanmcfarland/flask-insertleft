import markdown
import uuid
import base64

from datetime import datetime
from app import db

class WeaponMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), default="insert_name")
    weapon_type = db.Column(db.String(128), default="Ranged")
    bonus = db.Column(db.Integer,default=0)
    damage = db.Column(db.String(128), default="1d8")
    mag = db.Column(db.Integer, default=1)
    weapon_range = db.Column(db.String(128), default="200/400")
    attribute = db.Column(db.String(128), default="Dex")
    weight = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text, default="Enter additional information here...")

# database set-up for shootout sheets, allows each sheet to access user for each sheet
# e.g. sheet.author.username
class SheetMixin(object):
    id = db.Column(db.String(32), primary_key = True, nullable=False)
    name = db.Column(db.String(128), default="insert_name")
    character_class = db.Column(db.String(128), default="")
    background = db.Column(db.String(128), default="")
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    max_hp = db.Column(db.Integer,default=1)
    current_hp = db.Column(db.Integer,default=1)
    system_strain = db.Column(db.Integer, default=0)
    ac = db.Column(db.Integer, default=10)
    mental_save = db.Column(db.Integer, default=16)
    evasion_save = db.Column(db.Integer, default=16)
    physical_save = db.Column(db.Integer, default=16)
    strength = db.Column(db.Integer, default=0)
    dexterity = db.Column(db.Integer, default=0)
    constitution = db.Column(db.Integer, default=0)
    intelligence = db.Column(db.Integer, default=0)
    wisdom = db.Column(db.Integer, default=0)
    charisma = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=False, default='')   
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Everytime a new sheet is created, we automatically create a shorthand safe url using base64 and uuid
    # https://stackoverflow.com/questions/12270852/convert-uuid-32-character-hex-string-into-a-youtube-style-short-id-and-back
    def __init__(self, *args, **kwargs):
        super(SheetMixin, self).__init__(*args, **kwargs)
        self.id = self.uuid2urlsafe(uuid.uuid4().bytes)

    def uuid2urlsafe(self, uuid):
        return base64.urlsafe_b64encode(uuid).rstrip(b'=').decode('ascii')

    def urlsafe2uuid(self, urlstr):
        return str(uuid.UUID(bytes=base64.urlsafe_b64decode(urlstr + '==')))

    @classmethod
    def check_character_class(self, cls, bck):
        return cls in self.Config.classes and bck in self.Config.backgrounds

    @classmethod
    def append_weapon(self, weap):
        if not self.check_appended_weapon(weap):
            self.weapons.append(weap)

    @classmethod
    def remove_weapon(self, weap):
        if self.check_appended_weapon(weap):
            self.weapons.remove(weap)

    @classmethod
    def check_appended_weapon(self, weap):
        return self.weapons.filter(self.sw_rel.c.weapon_id == weap.id).count() > 0   

    ## Query weapon table and join identiier where sheet id = sheet_id in weapon_identifier table
    ## Role.query.filter(Role.user_permissions.any(id=1)).all()?
    def appended_weapons(self):
        weaps = self.Weapon.query.join(self.sw_rel, (self.sw_rel.c.weapon_id == self.Weapon.id)).filter(self.sw_rel.c.sheet_id == self.id)
        return weaps.all()

    ## return records that do not have rows in the association table
    def missing_weapons(self):
        weaps = self.Weapon.query.join(self.sw_rel, (self.sw_rel.c.weapon_id == self.Weapon.id)).filter(self.sw_rel.c.sheet_id == self.id)
        ids_found = []
        for i in weaps.all():
            ids_found.append(i.id)
        weaps = self.Weapon.query.filter(self.Weapon.id.notin_(ids_found)).all()
        return weaps

    # form is request.form from a POST request for sheet
    def remove_form_weapons(self, form):
        for i in self.appended_weapons():
            if form.get("delete"+str(i.id)):
                self.remove_weapon(i)

    # loops through the form list and checks for any matching weapon ids (using getlist)
    # will add relationship to the list to the sqlite database
    def append_form_weapons(self, form):
        if form['add']:
            for i in self.Weapon.query.filter(self.Weapon.id.in_(form.getlist('add'))).all():
                self.append_weapon(i)

    def output_md(self):
        self.notes=markdown.markdown(self.notes)

    def process_and_save(self, form):
        for k in [*form.data]:
            setattr(self, k, form[k].data)
        self.last_update = datetime.utcnow()
        if self.check_character_class(self.character_class, self.background):
            return self.save()
        else:
            return None

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            db.session.rollback()
            return None

    def __repr__(self):
        return '<Sheet {}>'.format(self.name)