# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..database.models.account import Account


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """

    username = StringField('Username', validators=[DataRequired()])
    type = SelectField('Pet', choices=["Bunny","Cheeto"],validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if Account.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')