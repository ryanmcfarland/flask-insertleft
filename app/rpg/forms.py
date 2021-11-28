from wtforms import Form, StringField, IntegerField
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
    submit = StringField('submit', validators=[InputRequired()])
    notes = StringField('notes')


class WeaponForm(Form):
    weapon = IntegerField('weapon', validators=[InputRequired()])
    delete = IntegerField('delete', validators=[InputRequired()])

