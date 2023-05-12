import pandas as pd
from app import db
from models import Bill
from sqlalchemy import create_engine

def import_csv_to_db(db, file_path):
    df = pd.read_csv(file_path)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df.to_sql(Bill.__tablename__, con=engine, if_exists='replace', index=False)

    for _, row in df.iterrows():
        bill = Bill(
            bill_number=row['Bill #'],
            st=row['st'],
            state=row['State'],
            session=row['Session'],
            introduced=row['Introduced'],
            latest_action=row['Latest Action'],
            latest_action_date=row['Latest Action Date'],
            primary_sponsor=row['Primary Sponsor'],
            Cosponsors=row['Cosponsors'],
            subject=row['Subject'],
            short_subject=row['Short Subject'],
            latest_bill_text_url=row['Latest Bill Text'],
            open_states_url=row['Link'],
            UniqueID=row['Unique ID']
        )
        db.session.add(bill)

    db.session.commit()

def import_analysis_csv_to_db(db, file_path):
    df = pd.read_csv(file_path)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df.to_sql(Analysis.__tablename__, con=engine, if_exists='replace', index=False)

    for _, row in df.iterrows():
        analysis = Analysis(
            bill_number=row['Bill Number'],
            state=row['Bill State'],
            session=row['Bill Session'],
            summary=row['Summary'],
            crypto_impact=row['Crypto Impact'],
            dcta_analysis=row['DCTA Analysis'],
            timestamp=row['timestamp']
        )
        db.session.add(analysis)

    db.session.commit()

def import_events_csv_to_db(db, file_path):
    df = pd.read_csv(file_path)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df.to_sql(Event.__tablename__, con=engine, if_exists='replace', index=False)

    for _, row in df.iterrows():
        event = Event(
            bill_number=row['Bill #'],
            st=row['St'],
            event_date=row['Latest Action Date'],
            action=row['Latest Action']
        )
        db.session.add(event)

    db.session.commit()