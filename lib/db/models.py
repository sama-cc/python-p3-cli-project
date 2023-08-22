from sqlalchemy import func
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class UserGame(Base):
#     __tablename__ = "user_games"

#     id = Column(Integer(), primary_key=True)
#     game_id = Column(ForeignKey('games.id'))
#     user_id = Column(ForeignKey('users.id'))

#     game = relationship('Game', back_populates='game_users')
#     user = relationship('User', back_populates='game_users')

#     def __repr__(self):
#         return f'UserGame(game_id={self.game_id}, ' + \
#             f'user_id={self.user_id})'

owned_game = Table(
    'owned_games',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True,
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    email = Column(String(), unique=True)
    region = Column(String())
    games = relationship('Game', secondary=owned_game, back_populates='users')
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'username="{self.username}", ' + \
            f'email="{self.email}", ' + \
            f'user_since="{self.created_at}", ' + \
            f'region="{self.region})"'

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())
    users = relationship('User', secondary=owned_game, back_populates='games')
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title="{self.title}", ' + \
            f'platform="{self.platform})"'
    

