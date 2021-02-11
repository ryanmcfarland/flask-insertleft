from wtforms import Form, StringField, IntegerField, validators
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from app.models import User


class SheetForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(max=128)])
    character_class = StringField('character_class', validators=[DataRequired(), Length(max=128)])
    background = StringField('background', validators=[DataRequired(), Length(max=128)])
    level = IntegerField('level', validators=[DataRequired()])
    xp = IntegerField('xp', validators=[DataRequired()])
    max_hp = IntegerField('max_hp', validators=[DataRequired()])
    current_hp = IntegerField('current_hp', validators=[DataRequired()])
    attack_bonus = IntegerField('attack_bonus', validators=[DataRequired()])
    system_strain = IntegerField('system_strain', validators=[DataRequired()])
    ac1 = IntegerField('ac1', validators=[DataRequired()])
    ac2 = IntegerField('ac2', validators=[DataRequired()])
    mental_save = IntegerField('mental_save', validators=[DataRequired()])
    evasion_save = IntegerField('evasion_save', validators=[DataRequired()])
    physical_save = IntegerField('physical_save', validators=[DataRequired()])
