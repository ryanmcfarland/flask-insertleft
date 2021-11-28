from app.rpg.forms import SheetForm

from wtforms import IntegerField 
from wtforms.validators import InputRequired

class StarsForm(SheetForm):
    administer = IntegerField('administer', validators=[InputRequired()])
    connect = IntegerField('connect', validators=[InputRequired()])
    exert = IntegerField('exert', validators=[InputRequired()])
    fix = IntegerField('fix', validators=[InputRequired()])
    heal = IntegerField('heal', validators=[InputRequired()])
    know = IntegerField('know', validators=[InputRequired()])
    lead = IntegerField('lead', validators=[InputRequired()])
    notice = IntegerField('notice', validators=[InputRequired()])
    perform = IntegerField('perform', validators=[InputRequired()])
    pilot = IntegerField('pilot', validators=[InputRequired()])
    program = IntegerField('program', validators=[InputRequired()])
    punch = IntegerField('punch', validators=[InputRequired()])
    shoot = IntegerField('shoot', validators=[InputRequired()])
    sneak = IntegerField('sneak', validators=[InputRequired()])
    stab = IntegerField('stab', validators=[InputRequired()])
    survive = IntegerField('survive', validators=[InputRequired()])
    talk = IntegerField('talk', validators=[InputRequired()])
    trade = IntegerField('trade', validators=[InputRequired()])
    work = IntegerField('work', validators=[InputRequired()])
    biopsionics = IntegerField('biopsionics', validators=[InputRequired()])     
    metapsionics = IntegerField('metapsionics', validators=[InputRequired()])     
    precognition = IntegerField('precognition', validators=[InputRequired()])    
    telekinesis = IntegerField('telekinesis', validators=[InputRequired()])     
    telepathy = IntegerField('telepathy', validators=[InputRequired()])
    teleportation = IntegerField('teleportation', validators=[InputRequired()])  
