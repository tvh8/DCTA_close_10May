import pandas as pd
from models import Bill, Analysis, Event
from database import db
from sqlalchemy.exc import IntegrityError

def import_csv_to_db(file_path):
    df = pd.read_csv(file_path)
    df.fillna('na', inplace=True)

    # Parse the date columns
    df['Introduced'] = pd.to_datetime(df['Introduced'], format='%b %d %Y', errors='coerce')
    df['Latest Action Date'] = pd.to_datetime(df['Latest Action Date'], format='%b %d %Y', errors='coerce')

    for _, row in df.iterrows():
        bill = Bill(
            bill_number=row['Bill #'] if row['Bill #'] != 'na' else 'na',
            st=row['St'] if row['St'] != 'na' else 'na',
            state=row['State'] if row['State'] != 'na' else 'na',
            session=row['Session'] if row['Session'] != 'na' else 'na',
            introduced=row['Introduced'] if pd.notnull(row['Introduced']) else None,
            latest_action=row['Latest Action'] if row['Latest Action'] != 'na' else 'na',
            latest_action_date=row['Latest Action Date'] if pd.notnull(row['Latest Action Date']) else None,
            primary_sponsor=row['Primary Sponsor'] if row['Primary Sponsor'] != 'na' else 'na',
            cosponsors=row['Cosponsors'] if row['Cosponsors'] != 'na' else 'na',
            subject=row['Subject'] if row['Subject'] != 'na' else 'na',
            short_subject=row['Short Subject'] if row['Short Subject'] != 'na' else 'na',
            latest_bill_text_url=row['Latest Bill Text'] if row['Latest Bill Text'] != 'na' else 'na',
            open_states_url=row['Link'] if row['Link'] != 'na' else 'na',
        )
        db.session.add(bill)

    db.session.commit()


def import_analysis_csv_to_db(file_path):
    df = pd.read_csv(file_path)
    df.fillna('na', inplace=True)

    # Parse the date column
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y %H:%M', errors='coerce')
    df = df.dropna(subset=['timestamp'])

    for _, row in df.iterrows():
        analysis = Analysis(
            bill_number=row['Bill Number'] if row['Bill Number'] != 'na' else 'na',
            summary=row['Summary'] if row['Summary'] != 'na' else 'na',
            crypto_impact=row['Crypto Impact'] if row['Crypto Impact'] != 'na' else 'na',
            dcta_analysis=row['DCTA Analysis'] if row['DCTA Analysis'] != 'na' else 'na',
            timestamp=row['timestamp'] if pd.notnull(row['timestamp']) else None
        )
        db.session.add(analysis)

    db.session.commit()
def import_events_csv_to_db(file_path):
    df = pd.read_csv(file_path)
    df.fillna('na', inplace=True)

    # Parse the date columns
    df['Introduced'] = pd.to_datetime(df['Introduced'], format='%b %d %Y', errors='coerce')
    df['Event Date'] = pd.to_datetime(df['Event Date'], format='%b %d %Y', errors='coerce')

    for _, row in df.iterrows():
        event = Event(
            bill_number=row['Bill #'] if row['Bill #'] != 'na' else 'na',
            st=row['St'] if row['St'] != 'na' else 'na',
            event_date=row['Event Date'] if pd.notnull(row['Event Date']) else None,
            action=row['Action'] if row['Action'] != 'na' else 'na'
        )
        db.session.add(event)

    db.session.commit()