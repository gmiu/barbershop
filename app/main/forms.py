from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Email


class ScheduleForm1(FlaskForm):
    services = SelectField('Select Service', choices=[], validators=[DataRequired()], default=None)
    barbers = SelectField('Select Barber', choices=[], validators=[DataRequired()], default=None)
    reservation_date = SelectField('Select Date', choices=[])
    submit = SubmitField('Select')


class ScheduleForm2(FlaskForm):
    hours = SelectField('Select Hour', choices=[], validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Select')


class ConfirmForm(FlaskForm):
    submit = SubmitField('Confirm')
