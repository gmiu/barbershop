from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SelectService(FlaskForm):
    services = SelectField('Select Service', choices=[])
    barbers = SelectField('Select Barber', choices=[])
    submit1 = SubmitField('Select')
    date = SelectField('Select Date', choices=[])
    submit2 = SubmitField('Select')

