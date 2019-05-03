import json
import os
import sys

from sqlalchemy import create_engine
from selenium import webdriver

import config
from . import parser
from . import models
from . import dao
from . import settings
from . import constants
from .logging import parse_logger, log_messages


engine = create_engine(config.database_url)
parser_booster = os.environ.get('env') == 'prod' 
driver_options = settings.options if parser_booster else None
driver = webdriver.Chrome(config.chrome_driver_path, chrome_options=driver_options)

all_categories_path = os.path.join(config.data_path, 'all_categories.json')
parsed_categories_path = os.path.join(config.data_path, 'parsed_categories.json')
last_parsed_data_path = os.path.join(config.data_path, 'last_parsed_data.json')

class App:

    def __init__(self):
        self.parsed_categories = []
        self.category_page = 1


    def run(self):
        self.parse_all()


    def parse_all(self):
        
        last_parsed_data = self.get_last_parsed_data()
        last_category = last_parsed_data['last_category'] if last_parsed_data else None
        last_page = last_parsed_data['last_page'] if last_parsed_data else None

        categories = self.get_categories()

        if last_page:
            categories.insert(0, last_category)
            self.category_page = last_page

        for category in categories:
            try:
                self.parse_category(category)
            except Exception:
                parse_logger.logger.exception(log_messages.PARSE_ERROR.format(category, self.category_page))
                self.make_last_parsed_data(category, self.category_page)
                break
            else:
                self.parsed_categories.append(category)
                self.save_parsed_categories()


    def parse_category(self, category):
        driver.get(constants.PAGE_URL_SCELETON.format(category, self.category_page))
        html = driver.page_source
        while True :
            business_urls = parser.get_business_urls(html)
            db = dao.DAO(engine)
            for business_url in business_urls:
                if not db.is_url_duplicate(business_url):
                    driver.get(constants.PAGE_URL+business_url)
                    business = parser.get_business_contents(driver.page_source)
                    business[constants.Business.URL] = business_url
                    business[constants.Business.CATEGORY] = category
                    db.add(business)
            next_page_url = parser.get_next_page(html) 
            if not next_page_url:
                self.category_page = 1
                break
            else:
                driver.get(constants.PAGE_URL + next_page_url)
                html = driver.page_source
                self.category_page+=1


    def get_last_parsed_data(self):
        if os.path.isfile(last_parsed_data_path):
            with open(last_parsed_data_path) as json_file:
                data = json.load(json_file)
            return data

    def get_categories(self):

        with open(all_categories_path) as json_file:
            data = json.load(json_file)
            all_categories = data['all_categories']

        if os.path.isfile(parsed_categories_path):
            with open(parsed_categories_path) as json_file:
                data = json.load(json_file)
                self.parsed_categories = data['parsed_categories']

        return list(set(all_categories)-set(self.parsed_categories))


    def make_last_parsed_data(self, category, page):
        data = {'last_category':category, 'last_page':page}
        with open(last_parsed_data_path, 'w') as outfile:
            json.dump(data, outfile)


    def save_parsed_categories(self):
        data = {'parsed_categories':self.parsed_categories}
        with open(parsed_categories_path, 'w') as outfile:
            json.dump(data, outfile)



