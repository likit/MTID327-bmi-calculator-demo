from flask import Flask, request, render_template
from forms import ContactForm, BMIForm
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

app = Flask(__name__) # app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmi.db'
db.init_app(app)

from models import *

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/message', methods=['GET', 'POST'])
def leave_message():
    if request.method == 'POST':
        message = request.form['message']
        name = request.form.get('name') or 'Anonymous'
        return f'{name} said <em>"{message}"</em>.'
        
    return render_template('message_form.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        product = form.products.data
        return f'Thank you, {name}. We will contact you about {product} at {email}.'
    return render_template('contact_form.html', form=form)


@app.route('/bmi', methods=['GET', 'POST'])
def calculate_bmi():
    form = BMIForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        height = form.height.data
        height = height / 100
        weight = form.weight.data
        bmi = weight / (height ** 2)
        category = ''
        if bmi < 18.5:
            category = 'Underweight'
        elif bmi < 25:
            category = 'Normal weight'
        elif bmi < 30:
            category = 'Overweight'
        else:
            category = 'Obesity'
        bmi_record = BMIRecord(name=name,
                               height=height,
                               weight=weight,
                               bmi=bmi,
                               category=category)
        db.session.add(bmi_record)
        db.session.commit()
        return render_template('bmi-result.html',
                               name=name,
                               bmi=bmi,
                               height=height,
                               weight=weight,
                               category=category)
    return render_template('bmi-form.html', form=form)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
