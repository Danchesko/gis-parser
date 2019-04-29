import os
import json
import unicodedata

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from . import settings
import config

PAGE_URL = 'https://2gis.kg'
PAGE_URL_SCELETON = 'https://2gis.kg/bishkek/search/{}/page/{}'
CATEGORIES_PATH = os.path.join(config.basedir, 'data', 'categories.json')

driver = webdriver.Chrome(ChromeDriverManager().install()) 

def parse_category(category):
    page = 1
    while True:
        driver.get(PAGE_URL_SCELETON.format(category, page))
        parse_page(driver.page_source)
        page+=1
        if page ==2:
            break # test

def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    link_tags = soup.find_all('a', href=lambda x: x and 'firm' in x 
    and 'district' not in x and 'firms' not in x)
    advert_urls = [url['href'] for url in link_tags]
    adverts = []
    for advert_url in advert_urls:
        driver.get(PAGE_URL+advert_url)
        adverts.append(parse_advert(driver.page_source))
    return adverts


def parse_advert(html):
    soup = BeautifulSoup(html, 'html.parser')
    advert = {}
    title = soup.find('h1')
    advert['title'] = title.text if title else None
    numbers = soup.find_all('a', href = lambda x: x and 'tel:' in x)
    advert['numbers'] = list(set([number['href'][4:] for number in numbers]))
    address = soup.find('a', lambda x: x and 'address' in x)
    advert['address'] = unicodedata.normalize("NFKD", address.text) if address else None
    instagram = soup.find('a', lambda x: x and 'instagram' in x)
    advert['instagram'] = instagram['href'] if instagram else None
    email = soup.find('a', href = lambda x: x and 'mailto:' in x)
    advert['email'] = email.text if email else None
    website = soup.find('a', lambda x: x and 'website' in x) or \
        soup.find('a', lambda x: x and 'contact' in x,\
             href = lambda x: x and ('http' in x or 'https' in x))
    website_url = website['href'].split("://") if website else None 
    advert['website'] = website_url[-1] if website_url \
        and len(website_url) > 2 else None
    print(advert)
    return advert


if __name__ == '__main__':
    with open(CATEGORIES_PATH) as json_file:
        data = json.load(json_file)
    categories = data['all_categories']
    for category in categories:
        parse_category(category)






