from app import db
from app.rpg.beatcops import Config
from app.rpg.models import SheetMixin, WeaponMixin

## Many-to-many relationship table between weapon and sheet
## allows for a sheet to have multiple weapons
beatcops_weapon_identifier = db.Table('beatcops_weapon_identifier',
    db.Column('sheet_id', db.Integer, db.ForeignKey('beatcops_sheet.id')),
    db.Column('weapon_id', db.Integer, db.ForeignKey('beatcops_weapon.id'))
)

class BeatCopsWeapon(WeaponMixin, db.Model):
    __tablename__="beatcops_weapon"


class BeatCopsSheet(SheetMixin, db.Model):
    __tablename__="beatcops_sheet"
    administer = db.Column(db.Integer, default=-1)
    animal_handling = db.Column(db.Integer, default=-1)
    connect = db.Column(db.Integer, default=-1)
    drive = db.Column(db.Integer, default=-1)
    exert = db.Column(db.Integer, default=-1)
    fix = db.Column(db.Integer, default=-1)
    heal = db.Column(db.Integer, default=-1)
    investigate = db.Column(db.Integer, default=-1)
    know = db.Column(db.Integer, default=-1)
    lead = db.Column(db.Integer, default=-1)
    notice = db.Column(db.Integer, default=-1)
    perform = db.Column(db.Integer, default=-1)
    program = db.Column(db.Integer, default=-1)   
    punch = db.Column(db.Integer, default=-1)
    program = db.Column(db.Integer, default=-1)
    requisition = db.Column(db.Integer, default=-1)   
    search = db.Column(db.Integer, default=-1)
    shoot = db.Column(db.Integer, default=-1)   
    stealth = db.Column(db.Integer, default=-1)   
    strike = db.Column(db.Integer, default=-1)   
    survive = db.Column(db.Integer, default=-1)   
    talk = db.Column(db.Integer, default=-1)   
    work = db.Column(db.Integer, default=-1)     
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weapons = db.relationship("BeatCopsWeapon", secondary=beatcops_weapon_identifier, backref=db.backref('beatcops_weapon_identifier', lazy='dynamic'),lazy='dynamic')

    Config = Config
    Weapon = BeatCopsWeapon
    sw_rel = beatcops_weapon_identifier