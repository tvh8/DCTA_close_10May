import sys
print(sys.path)

from import_csv import import_csv_to_db, import_analysis_csv_to_db, import_events_csv_to_db
from app import create_app
from database import db

app = create_app()

with app.app_context():
    import_csv_to_db(db, 'output.csv')
    import_csv_to_db(db, 'analysis_output.csv')
    import_csv_to_db(db, 'events.csv')
    df.columns = df.columns.str.strip()