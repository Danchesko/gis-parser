from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


PAGE_URL = 'https://2gis.kg'

# options = webdriver.ChromeOptions()
# prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
#                             'plugins': 2, 'popups': 2, 'geolocation': 2, 
#                             'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
#                             'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
#                             'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
#                             'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
#                             'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
#                             'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
#                             'durable_storage': 2}}
# options.add_experimental_option('prefs', prefs)
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")


def parse_ad(html):
    soup = BeautifulSoup(html, 'html.parser')
    advert = {}
    advert['title'] = soup.find('h1').text
    advert['number'] =  list(set([contact['href'][4:] for contact in soup.find_all('a', href = lambda x: x and 'tel:' in x)]))
    return advert


if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(f'https://2gis.kg/bishkek/search/Поесть/page/1')
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    media_cards = [cards for cards in soup.find_all('a') if cards.has_attr('href')]
    urls = [card['href'] for card in media_cards if 'firm' in card['href'] and 'district' not in card['href']]
    for ad_url in urls:
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(PAGE_URL+ad_url)
        parse_ad(driver.page_source)





