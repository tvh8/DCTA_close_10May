from app import create_app
from database import db
from models import Bill, Analysis, Event
from import_csv import import_csv_to_db, import_analysis_csv_to_db, import_events_csv_to_db

app = create_app()

@app.cli.command("initdb")
def initdb():
    with app.app_context():
        db.create_all()
        import_csv_to_db('output.csv')
        import_analysis_csv_to_db('analysis_output.csv')
        import_events_csv_to_db('events.csv')
        print("Database initialized.")

@app.cli.command("dropdb")
def dropdb():
    with app.app_context():
        db.drop_all()
        print("Database dropped.")

if __name__ == '__main__':
    app.run(debug=True)