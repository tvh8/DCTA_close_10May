from DCTA.database import db
from sqlalchemy.dialects.sqlite import DATETIME

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.String(20), nullable=False)
    st = db.Column(db.String(20), nullable=False)
    session = db.Column(db.String(50), nullable=False)
    introduced = db.Column(db.DateTime)
    latest_action = db.Column(db.String(200))
    latest_action_date = db.Column(db.DateTime)
    primary_sponsor = db.Column(db.String(100))
    cosponsors = db.Column(db.String(500))
    subject = db.Column(db.String(200))
    short_subject = db.Column(db.String(30))
    open_states_url = db.Column(db.String(200))
    latest_bill_text_url = db.Column(db.String(200))

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(120), unique=True, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    crypto_impact = db.Column(db.Text, nullable=True)
    dcta_analysis = db.Column(db.Text, nullable=True)
    timestamp = db.Column(DATETIME, nullable=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    st = db.Column(db.String(20), nullable=False)
    event_date = db.Column(DATETIME, nullable=True)
    action = db.Column(db.Text, nullable=True)
