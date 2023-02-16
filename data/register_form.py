from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, IntegerField, \
    StringField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeated_password = PasswordField('Repeated password',
                                      validators=[DataRequired()])
    surname = StringField('Surname')
    name = StringField('Name')
    ago = IntegerField('Ago')
    submit = SubmitField('Submit')
