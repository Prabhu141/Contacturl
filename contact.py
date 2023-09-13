#this only working code 

import requests
from bs4 import BeautifulSoup
import phonenumbers
import re

# Function to extract the company website and contact us page URL
def extract_company_info(url):
    try:
        req = requests.get(url)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, "html.parser")

        # Find the company website
        company_website = url

        # Find the contact us page URL (you can modify the keywords as needed)
        contact_keywords = ["contact", "contact-us", "contactus", "get-in-touch", "about-us"]
        contact_us_url = None

        for link in soup.find_all("a", href=True):
            href = link["href"].lower()
            for keyword in contact_keywords:
                if keyword in href:
                    contact_us_url = link["href"]
                    if not contact_us_url.startswith("http"):
                        contact_us_url = url + contact_us_url

                    break

        return company_website, contact_us_url

    except Exception as e:
        return None, None

# Function to scrape contact information from a web page
def scrape_contact_info(url):
    try:
        req = requests.get(url)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, "html.parser")

        # Find common patterns for contact information (modify as needed)
        contact_elements = soup.find_all(["address", "div", "p", "span"])

        # Store unique contact information
        unique_contact_info = set()

        for element in contact_elements:
            text = element.get_text(strip=True)
            if text:
                unique_contact_info.add(text)

        # Join the unique contact information into a single string
        contact_text = "\n".join(unique_contact_info)

        return contact_text.strip()

    except Exception as e:
        return "Contact information not found"

# Function to extract mobile numbers and addresses from text
def extract_mobile_numbers_and_addresses(text):
    mobile_numbers = []
    addresses = []

    # Extract mobile numbers using a regular expression
    mobile_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    mobile_numbers.extend(mobile_pattern.findall(text))

    # Split the text into lines and check for addresses with more than three commas
    lines = text.split('\n')
    for line in lines:
        if line.count(',') > 3:
            addresses.append(line)

    return mobile_numbers, addresses

# Replace this URL with the URL of the company's website
company_url = "https://www.desss.com/"  # Replace with the actual URL

# Extract company website and contact us page URL
company_website, contact_us_url = extract_company_info(company_url)

if company_website and contact_us_url:
    print("Company Website:", company_website)
    print("Contact Us Page URL:", contact_us_url)

    # Scrape contact information from the contact us page
    contact_info = scrape_contact_info(contact_us_url)

    print("\nContact Information:")
    print(contact_info)

    # Extract and print mobile numbers and addresses
    mobile_numbers, addresses = extract_mobile_numbers_and_addresses(contact_info)

    if mobile_numbers:
        print("\nExtracted Mobile Numbers:")
        for mobile_number in mobile_numbers:
            print(mobile_number)

    if addresses:
        print("\nExtracted Addresses:")
        for address in addresses:
            print(address)
    else:
        print("No addresses or mobile numbers found in the contact information.")
else:
    print("Unable to extract company information.")
