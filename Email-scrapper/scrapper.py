import requests
import csv
from bs4 import BeautifulSoup
import json
import urllib.parse

base_url = "https://www.11880.com/suche/Handwerk/deutschland"
page_query_param = "page"
query_param = "query"
query_param_value = "cmxXakxKcWNvelMwbko5aFZ3YzdWemtjb0p5MFZ3YmtBRmp2b1RTbXFSOXZuekl3cVBWNnJsV3NuSkR2QnZWMlpUQXVMd3g1TUdxd1pKSXVaR3l5WlFOM0JHVjRCUVp2WVBXc3BUeXhWd2JsQUsxOVlQV21NSlNsTDJ1Q3BVRWNvMjVtVndjN3NGanZwelNoTVQ5Z0gySXlNUFY2b2FJZm9VMD0="

# Function to scrape emails from a given page
def scrape_emails_from_page(page):
    url = base_url + "?" + urllib.parse.urlencode({page_query_param: page, query_param: query_param_value})
    decoded_url = urllib.parse.unquote(url)
    print({decoded_url})
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print("OKOKOK")
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})

    emails = []
    for script in scripts:
        email_list = extract_emails_from_json(script.string)
        emails.extend(email_list)

    return emails

# Function to extract emails from JSON script
def extract_emails_from_json(json_script):
    emails = []
    try:
        data = json.loads(json_script)
        item_list = data["mainEntity"]["itemListElement"]
        for item in item_list:
            if "item" in item and "email" in item["item"]:
                email = item["item"]["email"]
                emails.append(email)
    except (KeyError, IndexError):
        pass
    return emails

# Main function to scrape emails from all pages and save to CSV
def scrape_emails_and_save_to_csv(num_pages):
    with open("emails.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Email"])

        for page in range(1, num_pages + 1):
            emails = scrape_emails_from_page(page)

            for email in emails:
                print(f"email: {email}")
                writer.writerow([email])

            print(f"Scraped page {page} of {num_pages}")

    print("Email scraping completed.")

# Specify the number of pages to scrape
num_pages = 2

# Start scraping emails and save to CSV
scrape_emails_and_save_to_csv(num_pages)
