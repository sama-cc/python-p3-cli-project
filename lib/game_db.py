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
click.option('--uname')
@click.pass_context
def register(ctx, uname):
    set_uname = click.prompt(f'\nWould you like to register as {uname}? y/n? Type "cancel" to cancel')
    if set_uname == "y" or "yes":
        p_email = click.prompt(f'\nPlease add your email address or hit "enter" to add it later.\n')
        p_region = click.prompt(f'\nPlease add your region or hit "enter" to add it later. \n')
        p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
        c_password = click.prompt(f'\nPlease confirm password', hide_input=True)

        p_match = True if c_password == p_password else False

        while not p_match:
            click.echo("\nPasswords did not match. Please try again.")
            p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
            c_password = click.prompt(f'\nPlease confirm password', hide_input=True)
            p_match = True if c_password == p_password else False        

        new_user = User(username=uname, email=p_email, region=p_region, password=p_password)
        
        confirm = click.prompt(f'\nIs this information correct?\nUsername: {uname}, Email: {p_email}, Region: {p_region}\nType "confirm" if it is correct to submit registration. Type "no" to input information again.')

        if confirm == "confirm":
            session.add(new_user)
            session.commit()

            click.echo(f'\n{new_user} has been successfully registered. Please log in.')
            ctx.invoke(login)
        else:
            ctx.invoke(register, uname=uname)        

    elif set_uname == "cancel":
        click.invoke(login)
    elif set_uname() == "n" or "no":
        p_user = click.prompt(f'\nPlease type your desired username.\n')
        e_user = session.query(User).filter(User.username == p_user).first()

        while e_user:
            click.echo(f"\n{p_user} is already taken. Please try again. ")
            p_user = click.prompt(f'\nPlease type your desired username.\n')
            e_user = session.query(User).filter(User.username == p_user).first()


        p_email = click.prompt(f'\nPlease add your email address or hit "enter" to add it later.\n')
        p_region = click.prompt(f'\nPlease add your region or hit "enter" to add it later. \n')
        p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
        c_password = click.prompt(f'\nPlease confirm password', hide_input=True)

        p_match = True if c_password == p_password else False

        while not p_match:
            click.echo("\nPasswords did not match. Please try again.")
            p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
            c_password = click.prompt(f'\nPlease confirm password', hide_input=True)

        new_user = User(username=p_user, email=p_email, region=p_region, password=p_password)

        confirm = click.prompt(f'\nIs this information correct?\nUsername: {p_user}, Email: {p_email}, Region: {p_region}\nType "confirm" if it is correct to submit registration. Type "no" to input information again.')

        if confirm == "confirm":
            session.add(new_user)
            session.commit()

            click.echo(f'\n{new_user} has been successfully registered. Please log in.')
            ctx.invoke(login)
        else:
            ctx.invoke(register, uname=uname) 

    else:
        click.echo("\nInvalid input. Please try again.")
        ctx.invoke(register, uname=uname)


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
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice == "platform":
        qplat = click.prompt("\nPlease choose from the following platforms: \n PC, Switch, Xbox, Playstation. \nQuery")
        result = [game for game in user.games if qplat in game.platform]

        if result:
            for game in result:
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)  
    elif choice == "genre":
        qgenre = click.prompt("\nPlease choose from the following genres: \n FPS, RPG, Adventure, Strategy, MOBA. \nQuery")
        result = [game for game in user.games if qgenre in game.genre]

        if result:
            for game in result:
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice == "price":
        qprice = click.prompt("\nPlease input price as an integer. \nQuery")
        result = [game for game in user.games if int(qprice) == game.price]

        if result:
            for game in result:
                click.echo(f"\n{game}")
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
@click.pass_context
def login(ctx, uname):
    """Login prompt"""
    user = session.query(User).filter(User.username == uname).first()
    if user:
        p_password = click.prompt(f'Password', hide_input=True)
        c_password = click.prompt(f'Confirm password', hide_input=True)

        p_match = True if c_password == p_password else False

        while not p_match:
            click.echo("\nPasswords did not match. Please try again.")
            p_password = click.prompt(f'Password', hide_input=True)
            c_password = click.prompt(f'Confirm password', hide_input=True)
            p_match = True if c_password == p_password else False

        if p_password == user.password:

            click.echo(f'\nWelcome {uname}. Loading your Game DB...')
            ctx.invoke(main, user=user)        
        else:
            click.echo('\nPassword did not match the record. Try again')
            ctx.forward(login)
    else:
        reg_prompt = click.prompt(f"\n{uname} is not in the list of registered usernames. Would you like to register now? y/n?")

        if reg_prompt == "y":
            ctx.invoke(register, uname=uname)
        elif reg_prompt == "n":
            ctx.forward(login) 



if __name__ == '__main__':
    
    login()
    


    