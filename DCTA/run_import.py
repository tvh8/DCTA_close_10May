from DCTA.import_csv import import_csv_to_db
from DCTA.app import create_app
from DCTA.database import db

app = create_app()

with app.app_context():
    import_csv_to_db(db, 'output.csv')
    import_csv_to_db(db, 'analysis_output.csv')
    import_csv_to_db(db, 'events.csv')
