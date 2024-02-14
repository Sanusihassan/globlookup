import requests
from bs4 import BeautifulSoup
import os
import re

# Function to scrape links from the Wikipedia page
def scrape_country_links(url):
    response = requests.get(url)
    if response.status_code ==  200:
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
                    if len(tds) >  1:  # Ensure there are at least two td elements
                        country_link = tds[1].find('a')
                        if country_link:
                            # Resolve the redirect if present
                            resolved_url = requests.head(f'https://en.wikipedia.org{country_link["href"]}').headers.get('location')
                            if resolved_url:
                                # Extract the page title from the resolved URL
                                page_title = resolved_url.split('/')[-1]
                                links.append((page_title, resolved_url))
                            else:
                                # If no redirect, just add the original link
                                links.append((country_link.text, f'https://en.wikipedia.org{country_link["href"]}'))
                return links
    return None



# Function to extract text content from a Wikipedia page

def extract_html(url):
    response = requests.get(url)
    if response.status_code ==  200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the main content element
        body_content = soup.find('div', id='bodyContent')
        if body_content:
            # Remove attributes from HTML elements
            for tag in body_content.find_all(True):
                tag.attrs = {}
            # Remove specific elements
            for unwanted_tag in body_content.find_all(['div', 'h2']):
                if unwanted_tag.text.strip().startswith(('From Wikipedia', 'External links', 'Categories', 'Retrieved from')):
                    unwanted_tag.decompose()
            # Remove hidden categories
            hidden_categories = body_content.find('div', class_='mw-hidden-catlinks')
            if hidden_categories:
                hidden_categories.decompose()
            # Return the HTML content as a string and the page title
            page_title = soup.title.string.replace(' - Wikipedia', '')
            return str(body_content), page_title
    return None, None



def sanitize_title(title):
    # Replace spaces with underscores
    sanitized_title = title.replace(' ', '_')
    # Remove any characters that are not alphanumeric, underscore, or hyphen
    sanitized_title = re.sub(r'[^a-zA-Z0-9_\-]', '', sanitized_title)
    return sanitized_title

# Function to save HTML content to a file
def save_to_html_file(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)



if __name__ == '__main__':
    base_url = 'https://en.wikipedia.org/wiki/List_of_country_calling_codes'
    country_links = scrape_country_links(base_url)
    if country_links:
        print("Found country links:")
        for page_title, country_url in country_links:
            html_content, actual_title = extract_html(country_url)
            if html_content and actual_title:
                sanitized_title = sanitize_title(actual_title)
                store_dir = './store/html'
                os.makedirs(store_dir, exist_ok=True)
                html_filename = os.path.join(store_dir, f'{sanitized_title}.html')  # Use sanitized_title as filename
                save_to_html_file(html_content, html_filename)
                print(f"Saved HTML content of {sanitized_title} to {html_filename}")
            else:
                print(f"Failed to extract HTML content of {page_title}")
    else:
        print("No country links found.")
