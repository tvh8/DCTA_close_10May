import requests
import csv
from bs4 import BeautifulSoup
import time

SEARCH_URL = "https://openstates.org/search/?query={}&page={}"

def parse_sponsors(soup):
    sponsors = soup.find_all("div", class_="card card--profile")
    primary_sponsor = ""
    cosponsors = []

    for sponsor in sponsors:
        sponsor_name = sponsor.find("h3", class_="card__heading").text.strip()
        sponsor_role = sponsor.find("div", class_="heading--xsmall").text.strip()

        if sponsor_role.lower() == "primary":
            primary_sponsor = sponsor_name
        elif sponsor_role.lower() == "cosponsor":
            cosponsors.append(sponsor_name)

    return primary_sponsor, cosponsors

def parse_latest_bill_text(soup):
    latest_bill_text_link = soup.find("a", class_="button", string="View Latest Bill Text")
    if latest_bill_text_link:
        return latest_bill_text_link["href"]
    else:
        return ""

def parse_bill_row(row):
    bill_link = row.find("a")
    bill_number = bill_link.text.strip()
    bill_url = "https://openstates.org" + bill_link["href"]
    state_session = row.find("span", class_="u-color--gray").text.strip()
    state_session_parts = state_session[1:-1].split(" - ")
    state = state_session_parts[0]
    session = state_session_parts[1]
    subject = row.find_all("span")[1].text.strip()
    introduced = row.find_all("td")[1].text.strip()
    latest_action = row.find_all("span")[2].text.strip()
    latest_action_date_element = row.find_all("td")[2].find("span", class_="u-color--gray")
    latest_action_date = latest_action_date_element.text.strip() if latest_action_date_element else ""

    # Navigate to the bill page and parse the primary sponsor, cosponsors, and latest bill text link
    bill_response = requests.get(bill_url)
    bill_soup = BeautifulSoup(bill_response.content, 'html.parser')
    primary_sponsor, cosponsors = parse_sponsors(bill_soup)
    latest_bill_text = parse_latest_bill_text(bill_soup)

    return {
        "Bill #": bill_number,
        "State": state,
        "Session": session,
        "Subject": subject,
        "Introduced": introduced,
        "Latest Action": latest_action,
        "Latest Action Date": latest_action_date,
        "Link": bill_url,
        "Primary Sponsor": primary_sponsor,
        "Cosponsors": "; ".join(cosponsors),
        "Latest Bill Text": latest_bill_text,
    }

def scrape_bills(query):
    bill_data = []

    for page in range(1, 21):
        response = requests.get(SEARCH_URL.format(query, page))
        soup = BeautifulSoup(response.content, 'html.parser')
        tbody = soup.find("tbody")

        if not tbody:
            break

        bill_rows = tbody.find_all("tr")

        for row in bill_rows:
            bill = parse_bill_row(row)
            bill_data.append(bill)

        time.sleep(1)

    return bill_data

def export_bills_to_csv(bill_data):
    with open('blockchain_cryptocurrency_bills.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Bill #', 'State', 'Session', 'Subject', 'Introduced', 'Latest Action', 'Latest Action Date', 'Link', 'Primary Sponsor', 'Cosponsors', 'Latest Bill Text'])

        for bill in bill_data:
            writer.writerow([bill['Bill #'], bill['State'], bill['Session'], bill['Subject'], bill['Introduced'], bill['Latest Action'], bill['Latest Action Date'], bill['Link'], bill['Primary Sponsor'], bill['Cosponsors'], bill['Latest Bill Text']])

    print("Data exported to 'blockchain_cryptocurrency_bills.csv'")

if __name__ == "__main__":
    blockchain_bills = scrape_bills("blockchain")
    cryptocurrency_bills = scrape_bills("cryptocurrency")
    digital_asset_bills = scrape_bills("digital asset")
    combined_bills = blockchain_bills + cryptocurrency_bills + digital_asset_bills
    export_bills_to_csv(combined_bills)