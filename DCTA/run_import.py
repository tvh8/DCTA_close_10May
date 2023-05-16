import sys
print(sys.path)

from import_csv import import_csv_to_db, import_analysis_csv_to_db, import_events_csv_to_db
from app import create_app
from database import db

app = create_app()

with app.app_context():
    db.create_all()
    import_csv_to_db('output.csv')
    import_analysis_csv_to_db('analysis_output.csv')
    import_events_csv_to_db('events.csv')