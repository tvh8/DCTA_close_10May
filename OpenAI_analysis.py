import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import csv
import openai
import sys
import re
import datetime

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
openai.api_key = "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"

def analyze_bill(latest_bill_text, bill_number, bill_state, bill_session):
    # Pass the bill text to the OpenAI API
    prompt = (
        f"Please analyze the following bill text, focusing on its impact on cryptocurrencies and blockchain technology: {latest_bill_text}\n\n"
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

    # Define a regular expression pattern to extract the required parts
    sections = ai_response.split("\n\n")

    if len(sections) == 3:
        summary = sections[0].strip()
        crypto_impact = sections[1].strip()
        dcta_analysis = sections[2].strip()
    else:
        summary = "Error: Unable to parse AI response for summary."
        crypto_impact = "Error: Unable to parse AI response for crypto impact."
        dcta_analysis = "Error: Unable to parse AI response for DCTA analysis."

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
                ["Bill Number", "Bill State", "Bill Session", "Summary", "Crypto Impact", "DCTA Analysis", "timestamp"])

        csv_writer.writerow([bill_number, bill_state, bill_session, summary, crypto_impact, dcta_analysis, timestamp])

    return summary, crypto_impact, dcta_analysis

if __name__ == "__main__":
    latest_bill_text = sys.argv[1]
    bill_number = sys.argv[2]
    bill_state = sys.argv[3]
    bill_session = sys.argv[4]
    analyze_bill(latest_bill_text, bill_number, bill_state, bill_session)
