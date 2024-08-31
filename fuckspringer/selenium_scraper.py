from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def initialize_driver(chrome_driver_path):
    # Set up the WebDriver service
    service = Service(executable_path=chrome_driver_path)
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service)
    return driver

def extract_journal_data(driver, url, template):
    # Load the page
    driver.get(url)
    # Let the page load completely
    driver.implicitly_wait(1)
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize the dictionary to store all the extracted data
    journal_data = {}

    # Extract data according to the provided template
    for key, extraction in template.items():
        if extraction.get('type') == 'single':
            element = soup.find(extraction['tag'], extraction['attributes'])
            journal_data[key] = element.get_text(strip=True) if element else None
        elif extraction.get('type') == 'list':
            elements = soup.find_all(extraction['tag'], extraction['attributes'])
            journal_data[key] = [el.get_text(strip=True) for el in elements] if elements else None
        elif extraction.get('type') == 'composite':
            composite_data = []
            elements = soup.find_all(extraction['tag'], extraction['attributes'])
            for element in elements:
                data = {}
                for sub_key, sub_extraction in extraction['sub_extractions'].items():
                    sub_element = element.find(sub_extraction['tag'], sub_extraction['attributes'])
                    data[sub_key] = sub_element.get_text(strip=True) if sub_element else None
                composite_data.append(data)
            journal_data[key] = composite_data if composite_data else None

    return journal_data

def extract_editorial_board(driver, url, editorial_template):
    # Load the page
    driver.get(url)
    # Let the page load completely
    driver.implicitly_wait(1)
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize the list to store editorial board information
    editorial_board = []

    # Extract the Editorial Board information
    editorial_board_section = soup.find('div', class_='right-pane')
    if editorial_board_section:
        editor_groups = editorial_board_section.find_all('div', class_='u-margin-xl-bottom')
        for section in editor_groups:
            role = section.find('h3', class_='js-editor-group-role').get_text(strip=True)
            for editor_group in section.find_all('div', 'editor-group'):
                name = editor_group.find('h4', class_='js-editor-name').get_text(strip=True)
                affiliation = editor_group.find('p', class_='js-affiliation').get_text(strip=True)
                img_tag = editor_group.find('img', class_='editor-img')
                image = img_tag['src'] if img_tag else None

                editorial_board.append({
                    'role': role,
                    'name': name,
                    'affiliation': affiliation,
                    'image': image if image else 'No image found',
                })

    return editorial_board

# Example usage
chrome_driver_path = "/usr/local/bin/chromedriver"  # Update this path if necessary
driver = initialize_driver(chrome_driver_path)

# Example templates for sciencedirect journal pages
sciencedirect_template = {
    'title': {'type': 'single', 'tag': 'h1', 'attributes': {'class': 'js-title-text'}},
    'editor': {'type': 'single', 'tag': 'h3', 'attributes': {'class': 'js-editor-name'}},
    'apc': {'type': 'single', 'tag': 'span', 'attributes': {'class': 'list-price u-h2'}},
    'time_to_first_decision': {'type': 'single', 'tag': 'div', 'attributes': {'class': 'value u-h2'}},
    'impact_factor': {'type': 'single', 'tag': 'span', 'attributes': {'class': 'text-l u-display-block'}},
    'citescore': {'type': 'single', 'tag': 'span', 'attributes': {'class': 'text-l u-display-block'}},
    'about_the_journal': {'type': 'single', 'tag': 'div', 'attributes': {'class': 'about-container'}},
    'calls_for_papers': {
        'type': 'composite',
        'tag': 'div',
        'attributes': {'class': 'item'},
        'sub_extractions': {
            'title': {'tag': 'h3', 'attributes': {'class': 'title'}},
            'guest_editors': {'tag': 'div', 'attributes': {'class': 'text-xs u-margin-xs-top u-clr-grey8'}},
            'description': {'tag': 'div', 'attributes': {'class': 'u-margin-xs-top text-s'}},
            'submission_deadline': {'tag': 'div', 'attributes': {'class': 'text-xs u-padding-xs-top'}}
        }
    }
}

# Extract journal data from the main page
journal_data = extract_journal_data(driver, 'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids', sciencedirect_template)

# Extract editorial board data from the editorial board page
editorial_board = extract_editorial_board(driver, 'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids/about/editorial-board', sciencedirect_template)

# Combine journal data with editorial board data
journal_data['editorial_board'] = editorial_board

# Close the WebDriver
driver.quit()

# The `journal_data` dictionary now contains all the extracted information
print(journal_data)