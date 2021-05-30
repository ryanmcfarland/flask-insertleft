from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length

class BlogForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(max=256)])
    caption = StringField('caption', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])