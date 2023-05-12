from database import db
from sqlalchemy.dialects.sqlite import DATETIME

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    bill_id = db.Column(db.String(100))
    state = db.Column(db.String(20), nullable=False)
    st = db.Column(db.String(20), nullable=False)
    session = db.Column(db.String(50), nullable=False)
    introduced = db.Column(db.DateTime)
    latest_action = db.Column(db.String(200))
    latest_action_date = db.Column(db.DateTime)
    primary_sponsor = db.Column(db.String(100))
    subjects = db.Column(db.String(200))
    title = db.Column(db.String(200))
    type = db.Column(db.String(50))
    url = db.Column(db.String(200))
    bill_status = db.Column(db.String(50))
    bill_text_url = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(120), unique=True, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    crypto_impact = db.Column(db.Text, nullable=True)
    dcta_analysis = db.Column(db.Text, nullable=True)
    timestamp = db.Column(DATETIME, nullable=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Assuming columns of the events.csv. Replace with your actual column names and types.
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    st = db.Column(db.String(20), nullable=False)
    event_date = db.Column(DATETIME, nullable=True)
    action = db.Column(db.Text, nullable=True)
