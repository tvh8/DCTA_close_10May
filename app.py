from flask import Flask, render_template, jsonify, request, json
import csv
import subprocess
import os
import pandas as pd
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bills', methods=['GET'])
def get_bills():
    csv_file = 'output.csv'
    with open('output.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        bills = [row for row in reader]

    json_data = json.dumps(bills)
    last_modified = datetime.fromtimestamp(os.path.getmtime(csv_file)).strftime('%m/%d/%Y %H:%M')
    print(json_data)
    return json_data, 200, {'Content-Type': 'application/json', 'Last-Modified': last_modified}

@app.route('/get_events', methods=['GET'])
def get_events():
    df = pd.read_csv('events.csv')
    return jsonify(df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/get_analysis/<bill_number>', methods=['GET'])
def get_analysis(bill_number):
    df = pd.read_csv('analysis_output.csv')
    if df.empty or bill_number not in df['Bill Number'].values:
        return jsonify({"error": "Bill analysis not found"}), 404
    bill_analysis = df[df['Bill Number'] == bill_number].iloc[0].to_dict()
    return jsonify(bill_analysis), 200


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
