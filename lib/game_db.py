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
@click.pass_context
def search(ctx, user):
    choice = click.prompt('\nHow would you like to search? \n Type "title" to search by title. \n Type "platform" to search by platform. \n Type "genre" to search by genre. \n Type "price" to search by price. \n Type "help" to view a full list of commands. \n Type "back" if you want to return to the previous menu. \n Type "exit" to exit the application.\n')

    if choice == "title":
        qtitle = click.prompt("Query")
        click.echo(f"\n {[game for game in user.games if qtitle in game.title]}")
        ctx.invoke(search, user=user)
    elif choice == "platform":
        click.echo(f"\n {user} \n")
        ctx.invoke(main, user=user)
    elif choice == "genre":
        click.echo(f"\n {user} \n")
        ctx.invoke(main, user=user)
    elif choice == "price":
        click.echo(f"\n {user} \n")
        ctx.invoke(main, user=user)
    elif choice == "back" or "..":
        ctx.invoke(main, user=user)
    elif choice == "help":
        click.echo("help")
    elif choice == "exit":
        click.echo("\n See you next time. \n")
        exit()
    else:
        click.echo("Input is not a valid option. Try 'help' for more options.")
        ctx.invoke(main, user=user)

cli.command()
click.option('--user')
@click.pass_context
def main(ctx, user):
    
    choice = click.prompt('\nWhat would you like to do? \n Type "games" to view your library. \n Type "search" if you want to search your library. \n Type "info" if you want to view your info. \n Type "help" to view a full list of commands. \n Type "exit" to exit the application\n')

    if choice == "games":
        click.echo(f"\n {[user.games]} \n")
        ctx.invoke(main, user=user)
    elif choice == "info":
        click.echo(f"\n {user} \n")
        ctx.invoke(main, user=user)
    elif choice == "search":
        ctx.invoke(search, user=user)
    elif choice == "help":
        click.echo("help")
    elif choice == "exit":
        click.echo("\n See you next time. \n")
        exit()
    else:
        click.echo("Input is not a valid option. Try 'help' for more options.")
        ctx.invoke(main, user=user)
    


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
    


    