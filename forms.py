from wtforms import Form, SelectField, StringField, EmailField, FloatField
from wtforms.validators import DataRequired


class ContactForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    products = SelectField('Products', choices=[
        ('A01', 'Aging'),
        ('W02', 'Wellness'),
        ('C01', 'Check Up'),
      ], validators=[DataRequired()]
    )


class BMIForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])