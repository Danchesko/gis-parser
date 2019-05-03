import json
import os

from sqlalchemy import create_engine
from selenium import webdriver

import config
from . import parser
from . import models
from . import dao
from . import settings
from . import constants


engine = create_engine(config.database_url)
parser_booster = os.environ.get('env') == 'prod' 
driver_options = settings.options if parser_booster else None
driver = webdriver.Chrome(config.chrome_driver_path, chrome_options=driver_options)

all_categories_path = os.path.join(config.data_path, 'all_categories.json')
parsed_categories_path = os.path.join(config.data_path, 'parsed_categories.json')

def run():
    print(get_categories())

def get_categories():

    with open(all_categories_path) as json_file:
        data = json.load(json_file)
        all_categories = data['all_categories']

    parsed_categories_file_exists = os.path.isfile(parsed_categories_path)
    parsed_categories = []
    if parsed_categories_file_exists:
        with open(parsed_categories_path) as json_file:
            data = json.load(json_file)
            parsed_categories = data['parsed_categories']

    return list(set(all_categories)-set(parsed_categories))

def parse_categories(categories):
    pass

