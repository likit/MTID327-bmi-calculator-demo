from wtforms import Form, SelectField, StringField, EmailField, FloatField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo


class ContactForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    products = SelectField('Products', choices=[
        ('A01', 'Aging'),
        ('W02', 'Wellness'),
        ('C01', 'Check Up'),
      ], validators=[DataRequired()]
    )


class BMIForm(FlaskForm):
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
