from sqlalchemy.orm import sessionmaker
from .models import DoubleGis
from .constants import Business
from .logging import logger, log_messages

class DAO():


    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def add(self, business):
        _business = DoubleGis(title=business[Business.TITLE],
                                    numbers=business[Business.NUMBERS],
                                    address=business[Business.ADDRESS],
                                    instagram=business[Business.INSTAGRAM],
                                    email=business[Business.EMAIL],
                                    website=business[Business.WEBSITE],
                                    html=business[Business.HTML],
                                    url=business[Business.URL])
        try:        
            self.session.add(_business)
            self.session.commit()
        except Exception:
            logger.logger.exception(log_messages.WRITE_ERROR)
            self.session.rollback()


    def is_url_duplicate(self, url):
        return bool(self.session.query(DoubleGis).get(url))
