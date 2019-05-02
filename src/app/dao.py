from sqlalchemy.orm import sessionmaker
from .models import DoubleGis
from .constants import Business

class DAO():

    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_one(self, business):
        
        self.session.add(DoubleGis(title=business[Business.TITLE],
                                numbers=business[Business.NUMBERS],
                                address=business[Business.ADDRESS],
                                instagram=business[Business.INSTAGRAM],
                                email=business[Business.EMAIL],
                                website=business[Business.WEBSITE],
                                html=business[Business.HTML],
                                url=business[Business.URL]))
        self.session.commit()
