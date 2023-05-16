from flask import Flask, render_template, jsonify, request, json
import csv
import subprocess
import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from database import db as _db  # use an alias to avoid conflict
from models import Bill, Analysis, Event
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

print(os.getcwd())
migrate = Migrate()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'DCTA.sqlite'),
    )

    # Additional configuration for SQLAlchemy
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    _db.init_app(app)  # Initialize SQLAlchemy with this app
    migrate.init_app(app, _db)  # And this for Flask-Migrate
    app.config['SQLALCHEMY_ECHO'] = True

    @app.cli.command("initdb")
    def initdb_command():
        # code to initialize the database goes here
        _db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_bills', methods=['GET'])
    def get_bills():
        # Query all bills from the database
        bills = Bill.query.all()

        # Convert the QuerySet to JSON
        bills_list = [
            {'bill_number': b.bill_number, 'state': b.state, 'st': b.st, 'session': b.session,
             'introduced': b.introduced, 'latest_action': b.latest_action, 'latest_action_date': b.latest_action_date,
             'primary_sponsor': b.primary_sponsor, 'subjects': b.subjects, 'title': b.title, 'type': b.type,
             'url': b.url, 'bill_status': b.bill_status, 'bill_text_url': b.bill_text_url, 'timestamp': b.timestamp} for
            b in bills]

        return jsonify(bills_list), 200

    @app.route('/get_events', methods=['GET'])
    def get_events():
        # Query all events from the database
        events = Event.query.all()

        # Convert the QuerySet to JSON
        events_list = [{'bill_number': e.bill_number, 'st': e.st, 'event_date': e.event_date, 'action': e.action} for e
                       in events]

        return jsonify(events_list), 200

    @app.route('/get_analysis/<bill_number>', methods=['GET'])
    def get_analysis(bill_number):
        # Query for the analysis with the specified bill number
        analysis = Analysis.query.filter_by(bill_number=bill_number).first()

        if analysis is None:
            return jsonify({"error": "Bill analysis not found"}), 404

        # Convert the Analysis object to a dictionary
        analysis_dict = {'bill_number': analysis.bill_number, 'summary': analysis.summary,
                         'crypto_impact': analysis.crypto_impact, 'dcta_analysis': analysis.dcta_analysis,
                         'timestamp': analysis.timestamp}

        return jsonify(analysis_dict), 200

    @app.route('/analyze', methods=['GET'])
    def analyze():
        latest_bill_text = request.args.get('latest_bill_text')
        bill_number = request.args.get('bill_number')
        bill_state = request.args.get('bill_state')
        bill_session = request.args.get('bill_session')

        # Execute the OpenAI_analysis.py script and capture its output
        result = subprocess.run(
            ['python', 'OpenAI_analysis.py', latest_bill_text, bill_number, bill_state, bill_session],
            capture_output=True, text=True)

        # Parse the output into a dictionary
        if result.stdout:
            # Split lines and get the last line which contains the JSON output
            lines = result.stdout.split('\n')
            output_line = lines[-1] if len(lines) > 0 else None
            if output_line:
                output_dict = json.loads(output_line)
                # Return the output as the response
                return jsonify(output_dict), 200
            else:
                return jsonify({"error": "No output from analysis script"}), 500

    @app.route('/create_letter/<billId>', methods=['GET'])
    def get_create_letter(billId):
        latest_bill_text = request.args.get('latest_bill_text')
        bill_number = request.args.get('bill_number')
        bill_state = request.args.get('bill_state')
        bill_session = request.args.get('bill_session')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
