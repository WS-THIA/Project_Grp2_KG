from wtforms import StringField, SubmitField, RadioField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class textInterface(FlaskForm):

    textInput = StringField('What would you like to eat??', validators=[DataRequired()])

    submitText = SubmitField('Feed ME!')

class radioInterface(FlaskForm):

    cuisine= RadioField('cuisine', choices = [('Asian','Asian'),
                                             ('Japanese','Japanese'),
                                             ('Westerm','Western'),
                                             ('Dessert','Dessert'),
                                             ('Western-Local','Western-Local'),
                                            ('Japanese-Local','Japanese-Local'),
                                            ('Western-Japanese','Western-Japanese')], validators=[DataRequired()])

    submitRadio = SubmitField('Feed ME!')

class recommendationInterface(FlaskForm):

    userID = StringField('Who would you like to make a recommendation to?', validators=[DataRequired()])

    submitRecommend = SubmitField("Recommend!")

