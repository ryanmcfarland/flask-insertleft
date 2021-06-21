from wtforms import Form, StringField
from wtforms.validators import ValidationError, DataRequired, Email, Length

#https://mdbootstrap.com/docs/b4/jquery/forms/contact/

class ContactForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(min=4, max=128)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(max=128)])
    message = StringField('message', validators=[DataRequired()])


