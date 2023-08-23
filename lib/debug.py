from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Game, User

fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///db/user_game.db')
    Session = sessionmaker(bind=engine)
    session = Session()


    import ipdb; ipdb.set_trace()