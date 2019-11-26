from wtforms import StringField, SubmitField, RadioField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class textInterface(FlaskForm):

    textInput = StringField('What would you like to eat??', validators=[DataRequired()])

    sortBy = RadioField('Order by...', choices = [('number_of_reviews','Number of Reviews'),('rating','Rating')],
                        validators=[DataRequired()])

    submitText = SubmitField('Feed ME!')

class radioInterface(FlaskForm):

    cuisine= RadioField('Which cuisine would you like to explore?', choices = [('Local','Asian'),
                                             ('Japanese','Japanese'),
                                             ('Western','Western'),
                                             ('Dessert','Dessert'),
                                             ('Western-Local','Western-Local'),
                                            ('Japanese-Local','Japanese-Local'),
                                            ('Western-Japanese','Western-Japanese')], validators=[DataRequired()])

    sortBy = RadioField('Order by...', choices = [('number_of_reviews','Number of Reviews'),('rating','Rating')],
                        validators=[DataRequired()])

    submitRadio = SubmitField('Feed ME!')

class recommendationInterface(FlaskForm):

    userID = StringField('Who would you like to make a recommendation to?', validators=[DataRequired()])

    submitRecommend = SubmitField("Recommend!")

