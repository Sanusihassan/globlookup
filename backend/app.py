import requests
from bs4 import BeautifulSoup
import os
import re

# Function to scrape links from the Wikipedia page
def scrape_country_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the section heading "Alphabetical order"
        section_heading = soup.find('span', id='Alphabetical_order')
        if section_heading:
            # Navigate to the next table element after the heading
            table = section_heading.find_next('table')
            if table:
                links = []
                rows = table.find_all('tr')
                for row in rows[1:]:
                    tds = row.find_all('td')
                    if len(tds) > 1:  # Ensure there are at least two td elements
                        country_link = tds[1].find('a')
                        if country_link:
                            country_link = country_link['href']
                            links.append(country_link)
                return links
    return None

# Function to extract text content from a Wikipedia page
def extract_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the main content element
        body_content = soup.find('div', id='bodyContent')
        if body_content:
            # Remove attributes from HTML elements
            for tag in body_content.find_all(True):
                tag.attrs = {}
            # Return the HTML content as a string
            return str(body_content)
    return None

# Function to save HTML content to a file
def save_to_html_file(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    base_url = 'https://en.wikipedia.org/wiki/List_of_country_calling_codes'
    country_links = scrape_country_links(base_url)
    if country_links:
        print("Found country links:")
        for country_link in country_links:
            country_url = f'https://en.wikipedia.org{country_link}'
            country_name = country_link.split('/')[-1]
            html_content = extract_html(country_url)
            if html_content:
                store_dir = './store/html'
                os.makedirs(store_dir, exist_ok=True)
                html_filename = os.path.join(store_dir, f'{country_name}.html')
                save_to_html_file(html_content, html_filename)
                print(f"Saved HTML content of {country_name} to {html_filename}")
            else:
                print(f"Failed to extract HTML content of {country_name}")
    else:
        print("No country links found.")
