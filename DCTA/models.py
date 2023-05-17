from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, UniqueConstraint, and_
from sqlalchemy.orm import relationship, backref
from database import db


class Analysis(db.Model):
    __tablename__ = 'analysis'

    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String)
    st = db.Column(db.String)
    session = db.Column(db.String)
    summary = db.Column(db.Text, nullable=True)
    crypto_impact = db.Column(db.Text, nullable=True)
    dcta_analysis = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True)

    bill_id = db.Column(db.Integer, ForeignKey('bill.id'))

    # Relationship with Bill
    bill = relationship("Bill", backref=backref("analyses", cascade="all, delete-orphan"))


class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String)
    st = db.Column(db.String)
    session = db.Column(db.String)
    state = db.Column(db.String(20), nullable=False)
    introduced = db.Column(db.DateTime)
    latest_action = db.Column('Latest Action', db.String(200))
    latest_action_date = db.Column('Latest Action Date', db.DateTime)
    primary_sponsor = db.Column('Primary Sponsor', db.String(100))
    cosponsors = db.Column(db.String(500))
    subject = db.Column(db.String(200))
    short_subject = db.Column('Short Subject', db.String(30))
    open_states_url = db.Column('Link', db.String(200))
    latest_bill_text_url = db.Column('Latest Bill Text', db.String(200))

    __table_args__ = (UniqueConstraint('bill_number', 'st', 'session', name='bill_unique'),)


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String)
    st = db.Column(db.String)
    session = db.Column(db.String)
    event_date = db.Column(db.DateTime, nullable=True)
    action = db.Column(db.Text, nullable=True)

    bill_id = db.Column(db.Integer, ForeignKey('bill.id'))

    # Relationship with Bill
    bill = relationship("Bill", backref=backref("events", cascade="all, delete-orphan"))
