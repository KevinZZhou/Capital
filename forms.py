from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import StringField
from wtforms.validators import InputRequired

class HistoricalTickerForm(FlaskForm):
    ticker = StringField('Stock Ticker', validators = [InputRequired()])
    submit = SubmitField('Submit')