import csv
import hashlib
import chardet
import os.path
from us_state_abbrev import us_state_abbrev

# Detect the encoding of the CSV file
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Load the data from the CSV file
input_file = 'blockchain_cryptocurrency_bills.csv'
output_file = 'output.csv'

encoding = detect_encoding(input_file)

# Read the existing output file if it exists
existing_data = {}
if os.path.isfile(output_file):
    with open(output_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            existing_data[row[0]] = row

data = []
unique_rows = set()
with open(input_file, newline='', encoding=encoding) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read the header row
    header.insert(2, 'St')  # Add a new column for the state abbreviation
    header.append('Unique ID')  # Add a new column for the unique ID
    header.insert(4, 'Short Subject')  # Insert a new column for the short subject

    for row in reader:
        state = row[1]
        if state == "United States":
            state_abbrev = "US"
        else:
            state_abbrev = us_state_abbrev.get(state, state)
        row.insert(2, state_abbrev)

        subject = row[4]
        if len(subject) > 25:
            short_subject = subject[:25] + "..."
        else:
            short_subject = subject
        row.insert(4, short_subject)  # Insert the short subject in the row

        # Remove duplicates by checking the uniqueness of the whole row
        row_str = ''.join(row)
        if row_str not in unique_rows:
            unique_rows.add(row_str)
            data.append(row)

# Add a unique ID to each row and update existing rows if necessary
for row in data:
    bill_id = row[0]
    if bill_id in existing_data:
        row.append(existing_data[bill_id][-1])  # Keep the existing unique ID
    else:
        unique_id = hashlib.sha1(''.join(row).encode('utf-8')).hexdigest()
        row.append(unique_id)

# Write the processed data to a new CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)

print(f"Processed data saved to {output_file}")