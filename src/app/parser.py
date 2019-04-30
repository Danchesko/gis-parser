import os
import unicodedata

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from src import settings
from .constants import Ad
from . import constants


class Parser:

    def __init__(self, parser_booster=False):
        driver_options = settings.options if parser_booster else None
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driver_options)
        self.category_page = 1
        self.businesses = []


    def parse_category(self, category, page=1):
        self.category_page = page
        self.driver.get(constants.PAGE_URL_SCELETON.format(category, self.category_page))
        while True:
            category_html = self.driver.page_source
            self.businesses.extend(self.parse_page(category_html))
            soup = BeautifulSoup(category_html, 'html.parser')
            current_page = soup.find('span', lambda x: x and 'pagination' in x and x.endswith('current'))
            next_page = current_page.find_next() if current_page else None
            next_page_url = next_page['href'] if next_page.has_attr('href') else None
            if next_page_url:
                self.driver.get(constants.PAGE_URL+next_page_url)
                self.category_page+=1
            else:
                return self.businesses


    def parse_page(self, html):
        businesses = []
        soup = BeautifulSoup(html, "html.parser")
        link_tags = soup.find_all('a', href=lambda x: x and 'firm' in x 
        and 'district' not in x and 'firms' not in x)
        business_urls = [url['href'] for url in link_tags]
        for business_url in business_urls:
            self.driver.get(constants.PAGE_URL+business_url)
            businesses.append(self.parse_business_contents(self.driver.page_source))
        return businesses


    def parse_business_contents(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        business = {}
        title = soup.find('h1')
        business[Ad.TITLE] = title.text if title else None
        numbers = soup.find_all('a', href = lambda x: x and 'tel:' in x)
        business[Ad.NUMBERS] = list(set([number['href'][4:] for number in numbers]))
        address = soup.find('a', lambda x: x and 'address' in x)
        business[Ad.ADDRESS] = unicodedata.normalize("NFKD", address.text) if address else None
        instagram = soup.find('a', lambda x: x and 'instagram' in x)
        business[Ad.INSTAGRAM] = instagram['href'] if instagram else None
        email = soup.find('a', href = lambda x: x and 'mailto:' in x)
        business[Ad.EMAIL] = email.text if email else None
        website = soup.find('a', lambda x: x and 'website' in x) or \
            soup.find('a', lambda x: x and 'contact' in x,\
                href = lambda x: x and ('http' in x or 'https' in x))
        website_url = website['href'].split("://") if website else None 
        business[Ad.WEBSITE] = website_url[-1] if website_url \
            and len(website_url) > 2 else None
        print(business)
        return business