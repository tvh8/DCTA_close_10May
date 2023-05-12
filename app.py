from flask import Flask, render_template, jsonify, request, json
import csv
import subprocess
import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from DCTA_troubleshoot.database import db
from DCTA_troubleshoot.models import Bill, Analysis, Event
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # SQLite database file location
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bills', methods=['GET'])
def get_bills():
    # Query all bills from the database
    bills = Bill.query.all()

    # Convert the QuerySet to JSON
    bills_list = [{'bill_number': b.bill_number, 'bill_id': b.bill_id, 'state': b.state, 'st': b.st, 'session': b.session, 'introduced': b.introduced, 'latest_action': b.latest_action, 'latest_action_date': b.latest_action_date, 'primary_sponsor': b.primary_sponsor, 'subjects': b.subjects, 'title': b.title, 'type': b.type, 'url': b.url, 'bill_status': b.bill_status, 'bill_text_url': b.bill_text_url, 'timestamp': b.timestamp} for b in bills]

    return jsonify(bills_list), 200

@app.route('/get_events', methods=['GET'])
def get_events():
    # Query all events from the database
    events = Event.query.all()

    # Convert the QuerySet to JSON
    events_list = [{'bill_number': e.bill_number, 'st': e.st, 'event_date': e.event_date, 'action': e.action} for e in events]

    return jsonify(events_list), 200

@app.route('/get_analysis/<bill_number>', methods=['GET'])
def get_analysis(bill_number):
    # Query for the analysis with the specified bill number
    analysis = Analysis.query.filter_by(bill_number=bill_number).first()

    if analysis is None:
        return jsonify({"error": "Bill analysis not found"}), 404

    # Convert the Analysis object to a dictionary
    analysis_dict = {'bill_number': analysis.bill_number, 'summary': analysis.summary, 'crypto_impact': analysis.crypto_impact, 'dcta_analysis': analysis.dcta_analysis, 'timestamp': analysis.timestamp}

    return jsonify(analysis_dict), 200


@app.route('/analyze', methods=['GET'])
def analyze():
    latest_bill_text = request.args.get('latest_bill_text')
    bill_number = request.args.get('bill_number')
    bill_state = request.args.get('bill_state')
    bill_session = request.args.get('bill_session')

    # Execute the OpenAI_analysis.py script and capture its output
    result = subprocess.run(['python', 'OpenAI_analysis.py', latest_bill_text, bill_number, bill_state, bill_session],
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


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
