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
driver = webdriver.Chrome(config.chrome_driver_path, chrome_options=settings.driver_options)

all_categories_path = os.path.join(config.data_path, 'all_categories.json')
parsed_categories_path = os.path.join(config.data_path, 'parsed_categories.json')
last_parsed_data_path = os.path.join(config.data_path, 'last_parsed_data.json')


class App:

    def __init__(self):
        self.parsed_categories = []
        self.current_category_page = 1
        self.current_category_name = ''


    def run(self):
        try:
            self.parse_all()
        except Exception:
            parse_logger.logger.exception(log_messages.PARSE_ERROR.format(self.current_category_name, self.current_category_page))
            self.save_last_parsed_data()


    def parse_all(self):
        
        last_parsed_data = self.get_last_parsed_data()
        last_category = last_parsed_data['last_category'] if last_parsed_data else None
        last_page = last_parsed_data['last_page'] if last_parsed_data else None

        categories = self.get_categories()

        if last_page:
            categories.remove(last_category)
            categories.insert(0, last_category)
            self.current_category_page = last_page

        for self.current_category_name in categories:
                self.parse_category()            
                self.parsed_categories.append(self.current_category_name)
                self.save_parsed_categories()
                
           


    def parse_category(self):
        driver.get(constants.PAGE_URL_SCELETON.format(self.current_category_name, self.current_category_page))
        html = driver.page_source
        while True :
            business_urls = parser.get_business_urls(html)
            db = dao.DAO(engine)
            for business_url in business_urls:
                if not db.is_url_duplicate(business_url):
                    driver.get(constants.PAGE_URL+business_url)
                    business = parser.get_business_contents(driver.page_source)
                    business[constants.Business.URL] = business_url
                    business[constants.Business.CATEGORY] = self.current_category_name
                    db.add(business)
            next_page_url = parser.get_next_page(html) 
            if not next_page_url:
                self.current_category_page = 1
                break
            else:
                driver.get(constants.PAGE_URL + next_page_url)
                html = driver.page_source
                self.current_category_page+=1


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


    def save_last_parsed_data(self):
        data = {'last_category':self.current_category_name, 'last_page':self.current_category_page}
        with open(last_parsed_data_path, 'w') as outfile:
            json.dump(data, outfile)


    def save_parsed_categories(self):
        data = {'parsed_categories':self.parsed_categories}
        with open(parsed_categories_path, 'w') as outfile:
            json.dump(data, outfile)



