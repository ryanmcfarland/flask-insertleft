from app.rpg.forms import SheetForm

from wtforms import IntegerField 
from wtforms.validators import InputRequired

class BeatCopsForm(SheetForm):
    administer = IntegerField('administer', validators=[InputRequired()])
    animal_handling = IntegerField('animal_handling', validators=[InputRequired()])
    connect = IntegerField('connect', validators=[InputRequired()])
    drive = IntegerField('drive', validators=[InputRequired()])
    exert = IntegerField('exert', validators=[InputRequired()])
    fix = IntegerField('fix', validators=[InputRequired()])
    heal = IntegerField('heal', validators=[InputRequired()])
    investigate = IntegerField('investigate', validators=[InputRequired()])
    know = IntegerField('know', validators=[InputRequired()])
    lead = IntegerField('lead', validators=[InputRequired()])
    notice = IntegerField('notice', validators=[InputRequired()])
    perform = IntegerField('perform', validators=[InputRequired()])
    program = IntegerField('program', validators=[InputRequired()])
    punch = IntegerField('punch', validators=[InputRequired()])
    requisition = IntegerField('requisition', validators=[InputRequired()])
    search = IntegerField('search', validators=[InputRequired()])
    shoot = IntegerField('shoot', validators=[InputRequired()])
    stealth = IntegerField('stealth', validators=[InputRequired()])
    strike = IntegerField('strike', validators=[InputRequired()])
    survive = IntegerField('survive', validators=[InputRequired()])    
    talk = IntegerField('talk', validators=[InputRequired()])
    work = IntegerField('work', validators=[InputRequired()])

