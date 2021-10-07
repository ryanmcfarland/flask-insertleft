import math
import markdown

from datetime import datetime
from app import db
from sqlalchemy.orm import reconstructor

## Many-to-many relationship table between weapon and sheet
## allows for a sheet to have multiple weapons
shootout_weapon_identifier = db.Table('shootout_weapon_identifier',
    db.Column('sheet_id', db.Integer, db.ForeignKey('shootout_sheet.id')),
    db.Column('weapon_id', db.Integer, db.ForeignKey('shootout_weapon.id'))
)


class ShootoutWeapon(db.Model):
    __tablename__="shootout_weapon"
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
class ShootoutSheet(db.Model):
    __tablename__="shootout_sheet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), default="insert_name")
    character_class = db.Column(db.String(128), default="")
    background = db.Column(db.String(128), default="")
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    max_hp = db.Column(db.Integer,default=1)
    current_hp = db.Column(db.Integer,default=1)
    system_strain = db.Column(db.Integer, default=0)
    ac = db.Column(db.Integer, default=10)
    strength = db.Column(db.Integer, default=0)
    dexterity = db.Column(db.Integer, default=0)
    constitution = db.Column(db.Integer, default=0)
    intelligence = db.Column(db.Integer, default=0)
    wisdom = db.Column(db.Integer, default=0)
    charisma = db.Column(db.Integer, default=0)
    administer = db.Column(db.Integer, default=0)
    cast_magic = db.Column(db.Integer, default=-1)
    connect = db.Column(db.Integer, default=-1)
    exert = db.Column(db.Integer, default=-1)
    fix = db.Column(db.Integer, default=-1)
    heal = db.Column(db.Integer, default=-1)
    horsemanship = db.Column(db.Integer, default=-1)
    know = db.Column(db.Integer, default=-1)
    know_magic = db.Column(db.Integer, default=-1)
    lead = db.Column(db.Integer, default=-1)
    notice = db.Column(db.Integer, default=-1)
    perform = db.Column(db.Integer, default=-1)
    punch = db.Column(db.Integer, default=-1)
    sail = db.Column(db.Integer, default=-1)   
    shoot = db.Column(db.Integer, default=-1)   
    sneak = db.Column(db.Integer, default=-1)   
    stab = db.Column(db.Integer, default=-1)   
    survive = db.Column(db.Integer, default=-1)   
    talk = db.Column(db.Integer, default=-1)   
    trade = db.Column(db.Integer, default=-1)   
    work = db.Column(db.Integer, default=-1)     
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weapons = db.relationship("ShootoutWeapon", secondary=shootout_weapon_identifier, backref=db.backref('shootout_weapon_identifier', lazy='dynamic'),lazy='dynamic')
    notes = db.Column(db.Text, nullable=False, default='')


    def check_character_class(self, cls, bck):
        return cls in self.classes and bck in self.backgrounds


    def update_bonuses(self):
        self.attack_bonus=math.ceil(self.level/2)
        self.str_mod=self.update_modifiers(self.strength)
        self.dex_mod=self.update_modifiers(self.dexterity)
        self.con_mod=self.update_modifiers(self.constitution)
        self.int_mod=self.update_modifiers(self.intelligence)
        self.wis_mod=self.update_modifiers(self.wisdom)
        self.chr_mod=self.update_modifiers(self.charisma)
        self.mental_save=16-self.level-(max(self.wis_mod, self.chr_mod))
        self.evasion_save=16-self.level-(max(self.int_mod, self.dex_mod))        
        self.physical_save=16-self.level-(max(self.con_mod, self.str_mod))

    def update_modifiers(self, attr):
        if attr < 4:
            return -2
        elif attr < 8:
            return -1
        elif attr < 14:
            return 0
        elif attr < 18:
            return 1
        else:
            return 2

    def append_weapon(self, weap):
        if not self.check_appended_weapon(weap):
            self.weapons.append(weap)
    
    def remove_weapon(self, weap):
        if self.check_appended_weapon(weap):
            self.weapons.remove(weap)

    def check_appended_weapon(self, weap):
        return self.weapons.filter(shootout_weapon_identifier.c.weapon_id == weap.id).count() > 0   

    ## Query weapon table and join identiier where sheet id = sheet_id in weapon_identifier table
    ## Role.query.filter(Role.user_permissions.any(id=1)).all()?
    def appended_weapons(self):
        weaps = ShootoutWeapon.query.join(shootout_weapon_identifier, (shootout_weapon_identifier.c.weapon_id == ShootoutWeapon.id)).filter(shootout_weapon_identifier.c.sheet_id == self.id)
        return weaps.all()

    ## return records that do not have rows in the association table
    def missing_weapons(self):
        weaps = ShootoutWeapon.query.join(shootout_weapon_identifier, (shootout_weapon_identifier.c.weapon_id == ShootoutWeapon.id)).filter(shootout_weapon_identifier.c.sheet_id == self.id)
        ids_found = []
        for i in weaps.all():
            ids_found.append(i.id)
        weaps = ShootoutWeapon.query.filter(ShootoutWeapon.id.notin_(ids_found)).all()
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
            for i in ShootoutWeapon.query.filter(ShootoutWeapon.id.in_(form.getlist('add'))).all():
                self.append_weapon(i)

    def output_md(self):
        self.notes=markdown.markdown(self.notes)

    def process_form(self, form):
        self.name=form.name.data
        self.character_class=form.character_class.data
        self.background=form.background.data
        self.level=form.level.data
        self.xp=form.xp.data
        self.max_hp=form.max_hp.data
        self.current_hp=form.current_hp.data
        self.system_strain=form.system_strain.data
        self.ac=form.ac.data
        self.strength=form.strength.data
        self.dexterity=form.dexterity.data
        self.constitution=form.constitution.data
        self.intelligence=form.intelligence.data
        self.wisdom=form.wisdom.data
        self.administer=form.administer.data
        self.cast_magic=form.cast_magic.data
        self.connect=form.connect.data
        self.exert=form.exert.data
        self.fix=form.fix.data
        self.heal=form.heal.data
        self.horsemanship=form.horsemanship.data
        self.know=form.know.data
        self.know_magic=form.know_magic.data
        self.lead=form.lead.data
        self.notice=form.notice.data
        self.perform=form.perform.data
        self.punch=form.punch.data
        self.sail=form.sail.data
        self.shoot=form.shoot.data
        self.sneak=form.sneak.data
        self.stab=form.stab.data
        self.talk=form.talk.data
        self.trade=form.trade.data
        self.work=form.work.data
        self.notes=form.notes.data

        return self.check_character_class(self.character_class, self.background)


    def __repr__(self):
        return '<Sheet {}>'.format(self.name)