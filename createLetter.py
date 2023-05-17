import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import csv
import openai
import sys
import re
import datetime
import json

timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
openai.api_key = "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"

def analyze_bill(latest_bill_text, bill_number, bill_state, bill_session):
    # Pass the bill text to the OpenAI API
    prompt = (
        f"Please analyze the following bill text, focusing on its impact on cryptocurrencies and blockchain technology: {latest_bill_text}\n\n"
        f"Given the following bill text, analyze how the Digital Currency Traders Alliance (DCTA) (https://joindcta.org/about/) "
        f"might view the bill, considering their mission to create a supportive environment "
        f"for digital currency traders and give a voice to everyday consumers: {latest_bill_text}\n\n"
        f"Here are examples of previous letters written by the DCTA:\n\n"
        f"[Example 1 - Support Letter] 'https://docs.google.com/document/d/1XmwrOnNqI0RwhfAvm03R-yNXuc-EPErL/edit?usp=share_link&ouid=115833259637411494201&rtpof=true&sd=true' \n\n"  # Add an example of a support letter here
        f"[Example 2 - Opposition Letter] 'https://docs.google.com/document/d/1FfOOChrzchp4bn4JGnrv_ya2z7ghPApM/edit?usp=share_link&ouid=115833259637411494201&rtpof=true&sd=true' \n\n"  # Add an example of an opposition letter here
        f"Based on these examples and the bill text, write a letter on behalf of the DCTA expressing support or opposition for the bill. [DCTA Letter]"
    )

    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1000, n=1, stop=None,
                                        temperature=0.5)

    # Extract the AI-generated response
    ai_response = response.choices[0].text.strip()
    print("AI response:", ai_response)

    # Parse the AI response
    dcta_analysis, dct_letter = parse_ai_response(ai_response)

    # Write DCTA Letter to a text file
    file_name = bill_number.replace(' ', '_') + '_' + bill_state.replace(' ', '_') + '_' + bill_session.replace(' ', '_') + '.txt'
    with open(file_name, 'w') as f:
        f.write(dct_letter)

def parse_ai_response(response):
    """
    Parse the AI response into the expected components
    """
    try:
        # Split the response based on the section labels
        dct_analysis_index = response.index('[DCTA Analysis]')
        dct_letter_index = response.index('[DCTA Letter]')

        # Extract each section from the response
        dcta_analysis = response[dct_analysis_index + len('[DCTA Analysis]'):dct_letter_index].strip()
        dct_letter = response[dct_letter_index + len('[DCTA Letter]'):].strip()
    except ValueError:  # Raised if one of the expected labels is not found in the response
        dcta_analysis = "Error: Unable to parse AI response for DCTA analysis."
        dct_letter = "Error: Unable to parse AI response for DCTA letter."

    return dcta_analysis, dct_letter
