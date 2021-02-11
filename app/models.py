from hashlib import md5
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sheets = db.relationship('Sheet', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), default="insert_name")
    character_class = db.Column(db.String(128), default="")
    background = db.Column(db.String(128), default="")
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    max_hp = db.Column(db.Integer,default=1)
    current_hp = db.Column(db.Integer,default=1)
    attack_bonus = db.Column(db.Integer,default=0)
    system_strain = db.Column(db.Integer, default=0)
    ac1 = db.Column(db.Integer, default=10)
    ac2 = db.Column(db.Integer,default=10)
    mental_save = db.Column(db.Integer,default=15)
    evasion_save = db.Column(db.Integer, default=15)
    physical_save = db.Column(db.Integer, default=15)
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

    def process_form(self, form):
        self.name=form.name.data
        self.character_class=form.character_class.data
        self.background=form.background.data
        self.level=form.level.data
        self.xp=form.xp.data
        self.max_hp=form.max_hp.data
        self.current_hp=form.current_hp.data
        self.attack_bonus=form.attack_bonus.data
        self.system_strain=form.system_strain.data
        self.ac1=form.ac1.data
        self.ac2=form.ac2.data
        self.mental_save=form.mental_save.data
        self.physical_save=form.physical_save.data
        self.evasion_save=form.evasion_save.data
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


    def __repr__(self):
        return '<Sheet {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
