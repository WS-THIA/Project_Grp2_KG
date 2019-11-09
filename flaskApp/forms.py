from wtforms import StringField, SubmitField, RadioField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class textInterface(FlaskForm):

    textInput = StringField('What would you like to eat??', validators=[DataRequired()])
    submitText = SubmitField('Feed ME!')

class radioInterface(FlaskForm):

    Gender = RadioField('Gender', choices = [('chinese','Chinese'),
                                             ('japanese','Japanese'),
                                             ('local','Local'),
                                             ('italian','Italian'),
                                             ('french','French')], validators=[DataRequired()])

    submitRadio = SubmitField('Feed ME!')