import os 

basedir = os.path.abspath(os.path.dirname(__file__))

chrome_driver_path = os.path.join(basedir, 'chrome_driver', 'chromedriver')

database_url = os.environ.get('DATABASE_URL')

data_path = os.path.join(basedir, 'data')

logs_path = os.path.join(basedir, 'logs')

chrome_remote_url = os.environ.get('CHROME_REMOTE_URL')

