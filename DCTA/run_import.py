import sys
print(sys.path)

from import_csv import import_csv_to_db, import_analysis_csv_to_db, import_events_csv_to_db
from app import create_app
from database import db
import pandas as pd
from models import Bill, Analysis, Event

app = create_app()

with app.app_context():
    db.create_all()
    import_csv_to_db('output.csv')
    import_analysis_csv_to_db('analysis_output.csv')
    import_events_csv_to_db('events.csv')

    df_analysis = pd.read_csv('analysis_output.csv')
    df_analysis = df_analysis.convert_dtypes()
    import_analysis_csv_to_db(db, df_analysis)

    df_events = pd.read_csv('events.csv')
    df_events = df_events.convert_dtypes()
    import_events_csv_to_db(db, df_events)
