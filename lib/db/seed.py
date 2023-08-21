#!/usr/bin/env python3

from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Game, User

fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///user_game.db')
    Session = sessionmaker(bind=engine)
    session = Session()

session.query(Game).delete()
session.query(User).delete()
session.commit()

region = ("US", "EU", "JP")
platform = ("Switch", "PC", "Xbox", "Playstaion")
genre = ("FPS", "RPG", "Adventure", "Strategy", "MOBA")

print("Seeding games and users...")

games = [
    Game(
        title=fake.unique.name(),
        genre=random.choice(genre),
        platform=random.choice(platform),
        price=random.randint(0, 60)
    )
for i in range(50)]

users = [
    User(
        username=fake.unique.name(),
        email=f"{fake.word()}@{fake.word()}.com",
        region=random.choice(region)        
    )
for i in range(50)]

session.add_all(games)
session.add_all(users)
session.commit()