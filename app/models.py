import math
import re
import markdown

from hashlib import md5
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from sqlalchemy import func
from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property



## Many-to-many relationship table between user and role
## allows for a user to have multiple roles
user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# User class, maps the user to multiple sheets, roles and blog entries
# Users can have multiple roles
# backref enables the Sheet/Posts model to access the user via sheet.author.id
# lowercase_username is a hybrid property and not a column, used to verify that username strings
# are not duplicated regardless of case (see offical sqlalchemy notes)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    verified = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary=user_permissions, backref=db.backref('user_permissions', lazy='dynamic'),lazy='dynamic')
    sheets = db.relationship('Sheet', backref='author', lazy='dynamic')
    posts = db.relationship('Entry', backref='author', lazy='dynamic')

    @hybrid_property
    def lowercase_username(self):
        return self.username.lower()
    
    @lowercase_username.expression
    def lowercase_username(cls):
        return func.lower(cls.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # enfore role list and return true or false
    def check_roles(self, roles):
        if not isinstance(roles, (list, tuple)):
            roles = [roles]
        return any (x in roles for x in self.get_roles())

    # loop through role values and print out list of roles attached to the user
    def get_roles(self):
        return [r[0] for r in  self.roles.values('name')]

    def append_role(self, role):
        r = Role.query.filter(Role.name.in_([role])).first()
        if not r:
            return None
        elif not self.check_appended_role(r):
            self.roles.append(r)

   
    def remove_role(self, role):
        r = Role.query.filter(Role.name.in_([role])).first()
        if not r:
            return None
        elif self.check_appended_role(r):
            self.roles.remove(r)


    def check_appended_role(self, role):
        return self.roles.filter(user_permissions.c.role_id == role.id).count() > 0   

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        self.name=self.name.capitalize()

    def __repr__(self):
        return '<Role {}>'.format(self.name)


## Many-to-many relationship table between tag and entry
attached_tags = db.Table('attached_tags',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


#https://github.com/eugenkiss/Simblin/blob/master/simblin/models.py
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, default="")
    slug = db.Column(db.String, unique=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    caption = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship("Tag", secondary=attached_tags, backref=db.backref('attached_tags', lazy='dynamic'), lazy='dynamic')

    def output_md(self):
        self.content=markdown.markdown(self.content, extensions=['attr_list', 'fenced_code'])
    
    def output_snapshot(self, snapshot):
        self.content="\n".join(self.content.split("\n")[:snapshot])
        
    def gen_slug(self):
        self.slug = re.sub(r'[^\w]+', '-', self.title.lower()).strip('-')
    
    # If False, always set published to False, return True for upstream checks
    # If true, check contents and return False if any fields empty
    # else set columns and return
    def publish(self, publish=True):
        if not publish:
            self.published=publish
            return True
        elif not self.title or not self.caption or not self.content:
            return False
        else:
            self.published=publish
            self.gen_slug()
            self.publish_date = datetime.utcnow()
            return True

    def __repr__(self):
        return '<Entry {}>'.format(self.title)


## Many-to-many relationship table between weapon and sheet
## allows for a sheet to have multiple weapons
weapon_identifier = db.Table('weapon_identifier',
    db.Column('sheet_id', db.Integer, db.ForeignKey('sheet.id')),
    db.Column('weapon_id', db.Integer, db.ForeignKey('weapon.id'))
)


class Weapon(db.Model):
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
class Sheet(db.Model):
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
    weapons = db.relationship("Weapon", secondary=weapon_identifier, backref=db.backref('weapons_identifier', lazy='dynamic'),lazy='dynamic')
    notes = db.Column(db.Text, nullable=False, default='')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_on_load()

    # These classes and backgrounds should be avilable to all sheets 
    @reconstructor
    def init_on_load(self):
        self.classes=["Warrior", "Expert", "Arcanist", "Magister", "Pact Maker", "Shaman", "War Mage", "Adepts", "Witch Hunter", "Martial Adept", "Mystic"]
        self.backgrounds=["Arcane Scholar", "Cleric", "Courtesan", "Cowhand", "Criminal", "Dilettante", "Engineer",
            "Entertainer", "Gentry", "Government Mage", "Hedge Wizard", "Hirespell", "Hunter", "Inquisitor", "Labourer",
            "Merchant", "Official", "Physician", "Politician", "Rogue Mage", "Scholar", "Soldier", "Thug", "Vagabond", "Worker"]

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
        return self.weapons.filter(weapon_identifier.c.weapon_id == weap.id).count() > 0   

    ## Query weapon table and join identiier where sheet id = sheet_id in weapon_identifier table
    ## Role.query.filter(Role.user_permissions.any(id=1)).all()?
    def appended_weapons(self):
        weaps = Weapon.query.join(weapon_identifier, (weapon_identifier.c.weapon_id == Weapon.id)).filter(weapon_identifier.c.sheet_id == self.id)
        return weaps.all()

    ## return records that do not have rows in the association table
    def missing_weapons(self):
        weaps = Weapon.query.join(weapon_identifier, (weapon_identifier.c.weapon_id == Weapon.id)).filter(weapon_identifier.c.sheet_id == self.id)
        ids_found = []
        for i in weaps.all():
            ids_found.append(i.id)
        weaps = Weapon.query.filter(Weapon.id.notin_(ids_found)).all()
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
            for i in Weapon.query.filter(Weapon.id.in_(form.getlist('add'))).all():
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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
