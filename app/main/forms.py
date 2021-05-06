from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length

class BlogForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(max=256)])
    content = StringField('content', validators=[DataRequired()])