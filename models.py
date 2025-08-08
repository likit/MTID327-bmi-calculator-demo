from main import db

class BMIRecord(db.Model):
  __tablename__ = 'bmi_records'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  height = db.Column(db.Float, nullable=False)
  weight = db.Column(db.Float, nullable=False)
  bmi = db.Column(db.Float, nullable=False)
  category = db.Column(db.String(50), nullable=False)