from bs4 import BeautifulSoup
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(f'https://2gis.kg/bishkek/search/Поесть/page/1')
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
media_cards = [cards for cards in soup.find_all('a') if cards.has_attr('href')]
urls = [card['href'] for card in media_cards if 'firm' in card['href'] and 'district' not in card['href']]




