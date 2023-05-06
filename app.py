from flask import Flask, render_template, jsonify, request, json
import csv
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bills', methods=['GET'])
def get_bills():
    with open('output.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        bills = [row for row in reader]

    json_data = json.dumps(bills)
    print(json_data)
    return json_data, 200, {'Content-Type': 'application/json'}


@app.route('/analyze', methods=['GET'])
def analyze():
    bill_number = request.args.get('bill_number')
    bill_state = request.args.get('bill_state')
    bill_session = request.args.get('bill_session')
    latest_bill_text = "Replace this with the bill text you want to analyze."

    try:
        result = subprocess.run(['python', 'OpenAI_analysis.py', latest_bill_text, bill_number, bill_state, bill_session],
                                stdout=subprocess.PIPE, text=True, timeout=60)
        return result.stdout, 200
    except subprocess.TimeoutExpired:
        return "The analysis process took too long and has timed out. Please try again later.", 408

@app.route('/get_summary_data', methods=['GET'])
def get_summary_data():
    bill_number = request.args.get('bill_number')
    summary_data = {}

    with open('analysis_output.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Bill Number'] == bill_number:
                summary_data = {
                    'bill_number': row['Bill Number'],
                    'summary': row['Summary'],
                    'crypto_impact': row['Crypto Impact'],
                    'dcta_analysis': row['DCTA Analysis'],
                    'timestamp': row['timestamp'],
                }

    return jsonify(summary_data)

if __name__ == '__main__':
    app.run(debug=True)
