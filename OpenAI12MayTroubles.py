import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import csv
import openai
import sys
import re
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Bill, Analysis

timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
openai.api_key = "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"

# Setup SQLAlchemy session
engine = create_engine('sqlite:///site.db')  # Update with your database path
Session = sessionmaker(bind=engine)
session = Session()

def analyze_bill(latestBillTextUrl, bill_number, st, session):
    # Pass the bill text to the OpenAI API
    prompt = (
        f"Please analyze the following bill text, focusing on its impact on cryptocurrencies and blockchain technology: {latestBillTextUrl}\n\n"
        f"Answer the following questions separately:\n\n"
        f"1. [Summary] Provide a detailed summary of the bill, including its purpose, "
        f"main provisions, and potential impact on cryptocurrencies and blockchain technology. Describe specifically how the bill proposes to accomplish its goals.\n"
        f"2. [Crypto Impact] Assess how the bill relates to cryptocurrency or blockchain technology. "
        f"Identify specific provisions and how they may impact the financial industry, technology, security, or digital asset mining. "
        f"If it does not directly relate to these topics, identify any indirect connections or reasons "
        f"why the bill might appear in a search for cryptocurrency or blockchain.\n"
        f"3. [DCTA Analysis] Analyze how the Digital Currency Traders Alliance (DCTA) (https://joindcta.org/about/) "
        f"might view the bill, considering their mission to create a supportive environment "
        f"for digital currency traders and give a voice to everyday consumers.")

    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1000, n=1, stop=None,
                                        temperature=0.5)

    # Extract the AI-generated response
    ai_response = response.choices[0].text.strip()
    print("AI response:", ai_response)
    # Parse the AI response
    summary, crypto_impact, dcta_analysis = parse_ai_response(ai_response)
    # Remove any newline characters from the extracted parts
    summary = summary.replace('\n', ' ')
    crypto_impact = crypto_impact.replace('\n', ' ')
    dcta_analysis = dcta_analysis.replace('\n', ' ')
    print(summary)
    print(crypto_impact)
    print(dcta_analysis)

    with open('analysis_output.csv', mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Check if the file is empty and add headers
        if csv_file.tell() == 0:
            csv_writer.writerow(
                ["Bill #", "St", "Session", "Summary", "Crypto Impact", "DCTA Analysis", "timestamp"])

        csv_writer.writerow(['SB 185', 'LA', '2023 Regular Session', summary, crypto_impact, dcta_analysis, timestamp])
    output_dict = {
        "Bill #": 'SB 185',
        "St": 'LA',
        "Session": '2023 Regular Session',
        "Summary": summary,
        "Crypto Impact": crypto_impact,
        "DCTA Analysis": dcta_analysis,
        "timestamp": timestamp,
    }
    # Print the dictionary as a JSON object
    print(json.dumps(output_dict))
def parse_ai_response(response):
    """
    Parse the AI response into the expected components
    """
    try:
        # Split the response based on the section labels
        summary_index = response.index('[Summary]')
        crypto_impact_index = response.index('[Crypto Impact]')
        dct_analysis_index = response.index('[DCTA Analysis]')
        # Extract each section from the response
        summary = response[summary_index + len('[Summary]'):crypto_impact_index].strip()
        crypto_impact = response[crypto_impact_index + len('[Crypto Impact]'):dct_analysis_index].strip()
        dcta_analysis = response[dct_analysis_index + len('[DCTA Analysis]'):].strip()
    except ValueError:  # Raised if one of the expected labels is not found in the response
        summary = "Error: Unable to parse AI response for summary."
        crypto_impact = "Error: Unable to parse AI response for crypto impact."
        dcta_analysis = "Error: Unable to parse AI response for DCTA analysis."

    return summary, crypto_impact, dcta_analysis

    print(json.dumps(output_dict))

    summary, crypto_impact, dcta_analysis = parse_ai_response(ai_response)
    analysis = Analysis(bill_id=bill_number, summary=summary, crypto_impact=crypto_impact, dcta_analysis=dcta_analysis,
                        timestamp=timestamp, )
    session.add(analysis)
    session.commit()

if __name__ == "__main__":
    latest_bill_text = 'https://www.legis.la.gov/Legis/ViewDocument.aspx?d=1313501'
    bill_number = 'SB 185'
    st = 'LA'
    session = '2023 Regular Session'
    analyze_bill(latest_bill_text, bill_number, st, session)
