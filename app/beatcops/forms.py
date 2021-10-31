from wtforms import Form, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length

class SheetForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(max=128)])
    character_class = StringField('character_class', validators=[DataRequired(), Length(max=128)])
    background = StringField('background', validators=[DataRequired(), Length(max=128)])
    level = IntegerField('level', validators=[InputRequired()])
    xp = IntegerField('xp', validators=[InputRequired()])
    max_hp = IntegerField('max_hp', validators=[InputRequired()])
    current_hp = IntegerField('current_hp', validators=[InputRequired()])
    system_strain = IntegerField('system_strain', validators=[InputRequired()])
    ac = IntegerField('ac', validators=[InputRequired()])
    mental_save = IntegerField('mental_save', validators=[InputRequired()])
    physical_save = IntegerField('physical_save', validators=[InputRequired()])
    evasion_save = IntegerField('evasion_save', validators=[InputRequired()])
    strength = IntegerField('strength', validators=[InputRequired()])
    dexterity = IntegerField('dexterity', validators=[InputRequired()])
    constitution = IntegerField('constitution', validators=[InputRequired()])
    intelligence = IntegerField('intelligence', validators=[InputRequired()])
    wisdom = IntegerField('wisdom', validators=[InputRequired()])
    charisma = IntegerField('charisma', validators=[InputRequired()])
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
    submit = StringField('submit', validators=[InputRequired()])
    notes = StringField('notes')


class WeaponForm(Form):
    weapon = IntegerField('weapon', validators=[InputRequired()])
    delete = IntegerField('delete', validators=[InputRequired()])

