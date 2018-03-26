from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    text = StringField(
        'text',
        validators=[DataRequired(), Length(max=140)],
        widget=TextArea())