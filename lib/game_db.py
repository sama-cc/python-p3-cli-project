import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Game, User

engine = create_engine('sqlite:///db/user_game.db')
Session = sessionmaker(bind=engine)
session = Session()

import click

cli=click.Group()

cli.command()
click.option('--user')
def main(user):
    choice = click.prompt('What would you like to do? Type "games" to view your library. Type "info" if you want to view your info. "--help" will give you a full list of commands.')

    if choice == "games":
        click.echo(user.games)
    elif choice == "info":
        click.echo(user)
    elif choice == "help":
        click.echo("get help")
    else:
        click.echo("Input is not a valid option. Try 'help' for more options.")
    


@cli.command()
@click.option('--uname', prompt='Welcome to Game DB. Please input your username',
              help='Input the username tied to your account')
@click.password_option()
@click.pass_context
def login(ctx, uname, password):
    """Login prompt"""
    user = session.query(User).filter(User.username == uname).first()
    if user:
        if user.password == password:
            click.echo(f'Welcome {uname}. Loading your Game DB...')
            ctx.invoke(main, user=user)        
    else:
        click.echo(f"Apologies. {uname} is not in the list of registered usernames. Would you like to register now?")


if __name__ == '__main__':
    
    login()
    


    