import os
import unicodedata
import sys

from bs4 import BeautifulSoup
from selenium import webdriver

from . import settings
from .constants import Business
from . import constants
import config


def get_next_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    current_page = soup.find('span', lambda x: x and 'pagination' in x and x.endswith('current'))
    next_page = current_page.find_next() if current_page else None
    next_page_url = next_page['href'] if next_page.has_attr('href') else None
    return next_page_url


def get_business_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    link_tags = soup.find_all('a', href=lambda x: x and 'firm' in x 
    and 'district' not in x and 'firms' not in x)
    business_urls = [url['href'] for url in link_tags]
    return business_urls


def get_business_contents(html):
    soup = BeautifulSoup(html, 'html.parser')
    business = {}
    title = soup.find('h1')
    business[Business.TITLE] = title.text if title else None
    numbers = soup.find_all('a', href = lambda x: x and 'tel:' in x)
    business[Business.NUMBERS] = list(set([number['href'][4:] for number in numbers]))
    address = soup.find('a', lambda x: x and 'address' in x)
    business[Business.ADDRESS] = unicodedata.normalize("NFKD", address.text) if address else None
    instagram = soup.find('a', lambda x: x and 'instagram' in x)
    business[Business.INSTAGRAM] = instagram['href'] if instagram else None
    email = soup.find('a', href = lambda x: x and 'mailto:' in x)
    business[Business.EMAIL] = email.text if email else None
    website = soup.find('a', lambda x: x and 'website' in x) or \
        soup.find('a', lambda x: x and 'contact' in x,\
            href = lambda x: x and ('http' in x or 'https' in x))
    website_url = website['href'].split("://") if website else None 
    business[Business.WEBSITE] = website_url[-1] if website_url \
        and len(website_url) > 2 else None
    business[Business.HTML] = str(soup.find('body'))
    return business