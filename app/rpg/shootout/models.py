from app import db
from app.rpg.models import WeaponMixin, SheetMixin
from app.rpg.shootout import Config

## Many-to-many relationship table between weapon and sheet
## allows for a sheet to have multiple weapons
shootout_weapon_identifier = db.Table('shootout_weapon_identifier',
    db.Column('sheet_id', db.Integer, db.ForeignKey('shootout_sheet.id')),
    db.Column('weapon_id', db.Integer, db.ForeignKey('shootout_weapon.id'))
)

class ShootoutWeapon(WeaponMixin, db.Model):
    __tablename__="shootout_weapon"

class ShootoutSheet(SheetMixin, db.Model):
    __tablename__="shootout_sheet"
    administer = db.Column(db.Integer, default=-1)
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
    weapons = db.relationship("ShootoutWeapon", secondary=shootout_weapon_identifier, backref=db.backref('shootout_weapon_identifier', lazy='dynamic'),lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    Config = Config
    Weapon = ShootoutWeapon
    sw_rel = shootout_weapon_identifier
