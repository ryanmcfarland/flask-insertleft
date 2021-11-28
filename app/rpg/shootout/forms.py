from app.rpg.forms import SheetForm

from wtforms import IntegerField 
from wtforms.validators import InputRequired

class ShootoutForm(SheetForm):
    administer = IntegerField('administer', validators=[InputRequired()])
    cast_magic = IntegerField('cast_magic', validators=[InputRequired()])
    connect = IntegerField('connect', validators=[InputRequired()])
    exert = IntegerField('exert', validators=[InputRequired()])
    fix = IntegerField('fix', validators=[InputRequired()])
    heal = IntegerField('heal', validators=[InputRequired()])
    horsemanship = IntegerField('horsemanship', validators=[InputRequired()])
    know = IntegerField('know', validators=[InputRequired()])
    know_magic = IntegerField('know_magic', validators=[InputRequired()])
    lead = IntegerField('lead', validators=[InputRequired()])
    notice = IntegerField('notice', validators=[InputRequired()])
    perform = IntegerField('perform', validators=[InputRequired()])
    punch = IntegerField('punch', validators=[InputRequired()])
    sail = IntegerField('sail', validators=[InputRequired()])
    shoot = IntegerField('shoot', validators=[InputRequired()])
    sneak = IntegerField('sneak', validators=[InputRequired()])
    stab = IntegerField('stab', validators=[InputRequired()])
    survive = IntegerField('survive', validators=[InputRequired()])
    talk = IntegerField('talk', validators=[InputRequired()])
    trade = IntegerField('trade', validators=[InputRequired()])
    work = IntegerField('work', validators=[InputRequired()])

