import json
import requests
from bs4 import BeautifulSoup
import os

def scrape_country_codes():
    url = 'https://en.wikipedia.org/wiki/List_of_country_calling_codes'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    country_codes = {}
    table = soup.find('table', class_='wikitable')
    if table:
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:  # Ensure there are at least two cells in the row
                country_name = cells[0].text.strip()
                country_code = cells[1].text.strip()
                country_codes[country_name] = country_code

    return country_codes

def save_to_json(data, filename):
    store_dir = './store'
    os.makedirs(store_dir, exist_ok=True)
    file_path = os.path.join(store_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# if __name__ == '__main__':
#     country_codes = scrape_country_codes()
#     save_to_json(country_codes, 'country_codes.json')
