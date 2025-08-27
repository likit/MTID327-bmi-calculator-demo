import os

from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from forms import ContactForm, BMIForm, UserForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
app = Flask(__name__)  # app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmi.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


from models import *

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            name = form.name.data

            _password_hash = generate_password_hash(password)

            user = User(name=name, username=username, password=_password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return f'{form.errors}'
    return render_template('auth/register_user.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))

    return redirect(url_for('register_user'))


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))



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


def calculate_and_interpret_bmi(height, weight):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = 'Underweight'
    elif bmi < 25:
        category = 'Normal weight'
    elif bmi < 30:
        category = 'Overweight'
    else:
        category = 'Obesity'

    return bmi, category


@app.route('/bmi', methods=['GET', 'POST'])
def calculate_bmi():
    category_query = request.args.get('category_query')
    query = BMIRecord.query.filter_by(user=current_user)
    if category_query:
        query = query.filter_by(category=category_query)

    records = query.all()  # load all records to a list

    form = BMIForm(request.form)
    if request.method == 'POST' and form.validate():
        height = form.height.data
        weight = form.weight.data
        bmi, category = calculate_and_interpret_bmi(height / 100.0, weight)
        bmi_record = BMIRecord(user=current_user,
                               height=height,
                               weight=weight,
                               bmi=bmi,
                               category=category)
        db.session.add(bmi_record)
        db.session.commit()
        return render_template('bmi-result.html',
                               name=current_user.name,
                               bmi=bmi,
                               height=height,
                               weight=weight,
                               category=category)
    return render_template('bmi-form.html', form=form, records=records)


@app.route('/bmi/<int:record_id>/edit', methods=['GET', 'POST'])
def edit_bmi(record_id):
    record = BMIRecord.query.get(record_id)
    form = BMIForm()
    if request.method == 'POST':
        if form.validate():
            height = form.height.data
            weight = form.weight.data
            bmi, category = calculate_and_interpret_bmi(height / 100.0, weight)
            print(bmi, category, height / 100.0, weight)

            record.height = height
            record.weight = weight
            record.bmi = bmi
            record.category = category
            record.name = form.name.data

            db.session.add(record)
            db.session.commit()
            return redirect(url_for('calculate_bmi'))
        else:
            return form.errors

    form.name.data = record.name
    form.height.data = record.height
    form.weight.data = record.weight

    return render_template('edit-bmi-form.html', form=form, record_id=record_id)


@app.route('/bmi/<int:record_id>/delete', methods=['GET', 'POST'])
def delete_bmi(record_id):
    record = BMIRecord.query.get(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('calculate_bmi'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
