from DCTA.import_csv import import_csv_to_db, import_analysis_csv_to_db, import_events_csv_to_db
from DCTA.app import create_app
from DCTA.database import db

app = create_app()

with app.app_context():
    import_csv_to_db(db, 'dcta/output.csv')
    import_csv_to_db(db, 'dcta/analysis_output.csv')
    import_csv_to_db(db, 'dcta/events.csv')
    df.columns = df.columns.str.strip()