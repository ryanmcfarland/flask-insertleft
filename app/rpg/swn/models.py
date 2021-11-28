from app import db
from app.rpg.models import WeaponMixin, SheetMixin
from app.rpg.swn import Config

## Many-to-many relationship table between weapon and sheet
## allows for a sheet to have multiple weapons
swn_weapon_identifier = db.Table('swn_weapon_identifier',
    db.Column('sheet_id', db.Integer, db.ForeignKey('swn_sheet.id')),
    db.Column('weapon_id', db.Integer, db.ForeignKey('swn_weapon.id'))
)

class StarsWeapon(WeaponMixin, db.Model):
    __tablename__="swn_weapon"

class StarsSheet(SheetMixin, db.Model):
    __tablename__="swn_sheet"
    administer = db.Column(db.Integer, default=-1)
    connect = db.Column(db.Integer, default=-1)
    exert = db.Column(db.Integer, default=-1)
    fix = db.Column(db.Integer, default=-1)
    heal = db.Column(db.Integer, default=-1)
    know = db.Column(db.Integer, default=-1)
    lead = db.Column(db.Integer, default=-1)
    notice = db.Column(db.Integer, default=-1)
    perform = db.Column(db.Integer, default=-1)
    pilot = db.Column(db.Integer, default=-1)
    program = db.Column(db.Integer, default=-1)
    punch = db.Column(db.Integer, default=-1)
    shoot = db.Column(db.Integer, default=-1)   
    sneak = db.Column(db.Integer, default=-1)   
    stab = db.Column(db.Integer, default=-1)   
    survive = db.Column(db.Integer, default=-1)   
    talk = db.Column(db.Integer, default=-1)   
    trade = db.Column(db.Integer, default=-1)   
    work = db.Column(db.Integer, default=-1)
    biopsionics = db.Column(db.Integer, default=-1)     
    metapsionics = db.Column(db.Integer, default=-1)     
    precognition = db.Column(db.Integer, default=-1)     
    telekinesis = db.Column(db.Integer, default=-1)     
    telepathy = db.Column(db.Integer, default=-1)
    teleportation = db.Column(db.Integer, default=-1)         
    weapons = db.relationship("StarsWeapon", secondary=swn_weapon_identifier, backref=db.backref('swn_weapon_identifier', lazy='dynamic'),lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    Config = Config
    Weapon = StarsWeapon
    sw_rel = swn_weapon_identifier
