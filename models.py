from flask_login import UserMixin

from main import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)


class BMIRecord(db.Model):
  __tablename__ = 'bmi_records'
  id = db.Column(db.Integer, primary_key=True)
  height = db.Column(db.Float, nullable=False)
  weight = db.Column(db.Float, nullable=False)
  bmi = db.Column(db.Float, nullable=False)
  category = db.Column(db.String(50), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('bmi_records'))
