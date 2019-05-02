import os 

basedir = os.path.abspath(os.path.dirname(__file__))

chrome_driver_path = os.path.join(basedir, 'chrome_driver', 'chromedriver')

database_url = os.environ.get('DATABASE_URL')

categories_path = os.path.join(basedir, 'data', 'categories.json')

