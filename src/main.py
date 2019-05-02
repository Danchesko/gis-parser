import json
import os

import config
from src.app import parser

CATEGORIES_PATH = os.path.join(config.basedir, 'data', 'categories.json')

    

if __name__ == '__main__':
    with open(CATEGORIES_PATH) as json_file:
        data = json.load(json_file)
    categories = data['all_categories']
    parser_booster = True if os.environ.get('env') == 'prod' else False
    parser = parser.Parser(parser_booster)
    parser.parse_category('Телеканалы')

#test
