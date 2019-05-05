from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from app.models import Barber


class NewBarberForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add barber')

    def validate_username(self, username):
        user = Barber.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class NewServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=0, max=300)])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    price = IntegerField('Price (RON)', validators=[DataRequired()])
    submit = SubmitField('Add service')
