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
    choice = click.prompt('\nHow would you like to search? \n Type "title" to search by title. \n Type "platform" to search by platform. \n Type "genre" to search by genre. \n Type "price" to search by price. \n Type "back" to return to the previous menu. \n')

    if choice == "title":
        qtitle = click.prompt("\nPlease input the title keyword.\nQuery")
        result = [game for game in user.games if qtitle in game.title]
        
        if result:
            for game in result:
                click.echo(f"\n{game}\n")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice == "platform":
        qplat = click.prompt("\nPlease choose from the following platforms: \n PC, Switch, Xbox, Playstation. \nQuery")
        result = [game for game in user.games if qplat in game.platform]

        if result:
            for game in result:
                click.echo(f"\n{game}\n")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)  
    elif choice == "genre":
        qgenre = click.prompt("\nPlease choose from the following genres: \n FPS, RPG, Adventure, Strategy, MOBA. \nQuery")
        result = [game for game in user.games if qgenre in game.genre]

        if result:
            for game in result:
                click.echo(f"\n{game}\n")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice == "price":
        qprice = click.prompt("\nPlease input price as an integer. \nQuery")
        result = [game for game in user.games if int(qprice) == game.price]

        if result:
            for game in result:
                click.echo(f"\n{game}\n")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice == "back" or "..":
        ctx.invoke(main, user=user)
    else:
        click.echo("\nInput is not a valid option. Please try again.")
        ctx.invoke(main, user=user)

cli.command()
click.option('--user')
@click.pass_context
def main(ctx, user):
    
    choice = click.prompt('\nWhat would you like to do? \n Type "games" to view your library. \n Type "search" if you want to search your library. \n Type "info" if you want to view your info. \n Type "exit" to exit the application\n')

    if choice == "games":
        click.echo(f"\n {[user.games]} \n")
        ctx.invoke(main, user=user)
    elif choice == "info":
        click.echo(f"\n {user} \n")
        ctx.invoke(main, user=user)
    elif choice == "search":
        ctx.invoke(search, user=user)
    elif choice == "exit":
        click.echo("\n See you next time. \n")
        exit()
    else:
        click.echo("Input is not a valid option. Please try again")
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
            click.echo(f'\nWelcome {uname}. Loading your Game DB...')
            ctx.invoke(main, user=user)        
    else:
        click.echo(f"\nApologies. {uname} is not in the list of registered usernames. Would you like to register now?")


if __name__ == '__main__':
    
    login()
    


    