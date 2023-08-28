import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Game, User

engine = create_engine('sqlite:///db/user_game.db')
Session = sessionmaker(bind=engine)
session = Session()

import click

region = ["US", "EU", "JP"]
platform = ["Switch", "PC", "Xbox", "Playstaion"]
genre = ["FPS", "RPG", "Adventure", "Strategy", "MOBA"]

cli=click.Group()

@cli.command()
@click.option('--user')
@click.option('--choice')
@click.pass_context
def library(ctx, user, choice):
    
    if choice == None:
        choice = click.prompt(f'\nWhat would you like to do with your game library?\n Type "all" to view all games in your library.\n Type "search" to search for a game in your library.\n Type "add" to add a game to your library.\n Type "remove" to remove a game from your library.\n Type "back" to return to the Main menu.\n')

    if choice.lower() == "all":
        click.echo("\nBelow is a full list of your owned games:")
        for game in user.games:
            click.echo(f"\n{game}")
        ctx.invoke(library, user=user)
    elif choice.lower() == "search":
        ctx.invoke(search, user=user) 
    elif choice.lower() == "add":
        id_prompt = click.prompt('\nInput the ID of the game you wish to add to your library.\n Type "search" if you would like to search for a game ID.\n Type "all" if you would like to view the full library of games.\n Type "back" to go to the previous menu.\n')

        if id_prompt.lower() == "search":
            ctx.invoke(search, user=user)
        elif id_prompt.lower() == "all":
            click.echo("Below is a complete list of the game catalogue:")
            cat = session.query(Game).all()
            for game in cat:
                click.echo(f'\n{game}')
            ctx.invoke(library, user=user, choice=choice)
        elif id_prompt.lower() == "back":
            ctx.invoke(main, user=user)
        else:
            try:                
                id = int(id_prompt)
                if id:
                    if id in [game.id for game in session.query(Game).all()]:
                        game = session.query(Game).filter(Game.id == id).first()
                        p_add = click.prompt(f'\nAdd the following game to your library? y/n?\n\n{game}\n\n')
                        if p_add.lower() == "y" or p_add.lower() == "yes":
                            game.users.append(session.query(User).filter(User.id==user.id).first())
                            session.commit()
                            click.echo(f'\n{game.title} successfully added to your library.\n\nReturning to Library Menu.')
                            ctx.invoke(library, user=user)
                        else:
                            ctx.invoke(library, user=user, choice=choice)
                    else:
                        click.echo('\nInput does not match a game id in the catalogue.\nPlease Try again.\n')
                        ctx.invoke(library, user=user, choice=choice)
            except ValueError:
                click.echo('\nInput is invalid. Please Try again.')          
                ctx.invoke(library, user=user, choice=choice)   
                
    elif choice.lower() == "remove":
        pass 
    elif choice.lower() == "back":
        ctx.invoke(main, user=user) 


@cli.command()
@click.option('--user')
@click.pass_context
def account(ctx, user):
    change = click.prompt(f'\nYour account info:\n\n{user}\n\n Type "username" to change username.\n Type "email" to change email address.\n Type "region" to change region.\n Type "back" to go back to the previous menu.\n')

    if change.lower() == "username":
        p_user = click.prompt(f'\nPlease type your desired username or type "cancel" to cancel change request.\n\nCurrent username: {user.username}\nNew username\n')
        e_user = session.query(User).filter(User.username == p_user).first()

        if p_user.lower() == "cancel":
            click.echo('\nReturning to Account Menu.')
            ctx.invoke(account, user=user) 
        while e_user:
            click.echo(f"\n{p_user} is already taken. Please try again. ")
            p_user = click.prompt(f'\nPlease type your desired username.\n\nCurrent username: {user.username}\nNew username\n')
            e_user = session.query(User).filter(User.username == p_user).first()
        
        confirm = click.prompt(f'\nChange username to {p_user}? y/n?\n')
        if confirm.lower() == "y" or confirm.lower() == "yes":
                p_password = click.prompt(f'\nPassword', hide_input=True)
                c_password = click.prompt(f'Confirm password', hide_input=True)

                p_match = True if c_password == p_password else False

                while not p_match:
                    click.echo("\nPasswords did not match. Please try again.")
                    p_password = click.prompt(f'\nPassword', hide_input=True)
                    c_password = click.prompt(f'Confirm password', hide_input=True)
                    p_match = True if c_password == p_password else False

                if p_password == user.password:

                    user.username = p_user
                    session.commit()

                    click.echo("\nChange Successful.")
                    ctx.invoke(account, user=user)
                else:
                    click.echo('\nPassword did not match the record. Try again')
                    ctx.forward(account)                

        else:
            click.echo('\nReturning to Account Menu.')
            ctx.invoke(account, user=user)                     
            
    elif change.lower() == "email":
        p_email = click.prompt(f'\nType new email address or type "cancel" to cancel change request.\n\nCurrent email: {user.email}\nNew email')

        if p_email.lower == "cancel":
            click.echo('\nReturning to Account Menu.')
            ctx.invoke(account, user=user)  
        elif p_email:
            while ("@" and "." not in p_email) or (p_email == True):
                p_email = click.prompt('\nInvalid email format. Please input a valid email address or press "enter" to skip.\nNew email')

            confirm = click.prompt(f'\nChange email to {p_email}? y/n?\n')
            if confirm.lower() == "y" or confirm.lower() == "yes":
                p_password = click.prompt(f'\nPassword', hide_input=True)
                c_password = click.prompt(f'Confirm password', hide_input=True)

                p_match = True if c_password == p_password else False

                while not p_match:
                    click.echo("\nPasswords did not match. Please try again.")
                    p_password = click.prompt(f'\nPassword', hide_input=True)
                    c_password = click.prompt(f'Confirm password', hide_input=True)
                    p_match = True if c_password == p_password else False

                if p_password == user.password:

                    user.email = p_email
                    session.commit()

                    click.echo("\nChange Successful.")
                    ctx.invoke(account, user=user)

                else:
                    click.echo('\nPassword did not match the record. Try again')
                    ctx.forward(account)

            else: 
                click.echo('\nReturning to Account Menu.')
                ctx.invoke(account, user=user)

        elif not p_email:
            rm_email = click.prompt('Remove email from account? y/n?')

            if rm_email.lower() == "y" or rm_email.lower() == "yes":
                p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
                c_password = click.prompt(f'Please confirm password', hide_input=True)

                p_match = True if c_password == p_password else False

                while not p_match:
                    click.echo("\nPasswords did not match. Please try again.")
                    p_password = click.prompt(f'\nPassword', hide_input=True)
                    c_password = click.prompt(f'Confirm password', hide_input=True)
                    p_match = True if c_password == p_password else False

                user.email = ""
                session.commit()
            else:
                click.echo('\nReturning to Account Menu.')
                ctx.invoke(account, user=user)
        else:
            click.echo('\nReturning to Account Menu.')
            ctx.invoke(account, user=user)
    elif change.lower() == "region":
        p_region = click.prompt(f'\nType new region or type "cancel" to cancel change request. Accepted regions are "US", "EU, "JP". \n\nCurrent region: {user.region}\nNew region')

        if p_region.lower == "cancel":
            click.echo('\nReturning to Account Menu.')
            ctx.invoke(account, user=user)  
        elif p_region:
            while (p_region not in region) or (p_region == True):
                p_region = click.prompt('\nInvalid region. Accepted regions are "US", "EU, "JP" or press "enter" to skip.\nNew region')

            confirm = click.prompt(f'\nChange region to {p_region}? y/n?\n')
            if confirm.lower() == "y" or confirm.lower() == "yes":
                p_password = click.prompt(f'\nPassword', hide_input=True)
                c_password = click.prompt(f'Confirm password', hide_input=True)

                p_match = True if c_password == p_password else False

                while not p_match:
                    click.echo("\nPasswords did not match. Please try again.")
                    p_password = click.prompt(f'\nPassword', hide_input=True)
                    c_password = click.prompt(f'Confirm password', hide_input=True)
                    p_match = True if c_password == p_password else False

                if p_password == user.password:

                    user.region = p_region
                    session.commit()

                    click.echo("\nChange Successful.")
                    ctx.invoke(account, user=user)

                else:
                    click.echo('\nPassword did not match the record. Try again')
                    ctx.forward(account)

            else: 
                click.echo('\nReturning to Account Menu.')
                ctx.invoke(account, user=user)

        elif not p_email:
            rm_email = click.prompt('Remove email from account? y/n?')

            if rm_email.lower() == "y" or rm_email.lower() == "yes":
                p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
                c_password = click.prompt(f'Please confirm password', hide_input=True)

                p_match = True if c_password == p_password else False

                while not p_match:
                    click.echo("\nPasswords did not match. Please try again.")
                    p_password = click.prompt(f'\nPassword', hide_input=True)
                    c_password = click.prompt(f'Confirm password', hide_input=True)
                    p_match = True if c_password == p_password else False

                user.email = ""
                session.commit()
            else:
                click.echo('\nReturning to Account Menu.')
                ctx.invoke(account, user=user)
        else:
            click.echo('\nReturning to Account Menu.')
            ctx.invoke(account, user=user)
    elif change.lower() == "back":
        ctx.invoke(main, user=user)
    else:
        click.echo("\nInput is invalid.")
        ctx.invoke(account, user=user)

@cli.command()
@click.option('--uname')
@click.pass_context
def register(ctx, uname):
    set_uname = click.prompt(f'\nWould you like to register as {uname}? y/n? Type "cancel" to cancel')
    if set_uname.lower() == "y" or set_uname.lower() == "yes":
        p_email = click.prompt(f'\nPlease add your email address or hit "enter" to add it later.\n', default="")
        if p_email:
            while ("@" and "." not in p_email) or (p_email == True):
                p_email = click.prompt('\nInvalid email format. Please input a valid email address or press "enter" to skip.\n')

        p_region = click.prompt(f'\nPlease add your region as either "US", "EU", "JP" or hit "enter" to add it later. \n', default="")
        if p_region:
            while (p_region not in region) or (p_region == True):
                p_region = click.prompt('\nInvalid region. Please input "US", "EU", "JP" or press "enter" to skip.\n')

        p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
        c_password = click.prompt(f'Please confirm password', hide_input=True)

        p_match = True if c_password == p_password else False

        while not p_match:
            click.echo("\nPasswords did not match. Please try again.")
            p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
            c_password = click.prompt(f'Please confirm password', hide_input=True)
            p_match = True if c_password == p_password else False        

        new_user = User(username=uname, email=p_email, region=p_region, password=p_password)
        
        confirm = click.prompt(f'\nIs this information correct?\n\nUsername: {uname}, Email: {p_email}, Region: {p_region}\n\nType "confirm" if it is correct to submit registration. Type "no" to input information again.\n')

        if confirm.lower() == "confirm":
            session.add(new_user)
            session.commit()

            click.echo(f'\n{new_user} has been successfully registered. Please log in.')
            ctx.invoke(login, uname=uname)
        else:
            ctx.invoke(register, uname=uname)        

    elif set_uname.lower() == "cancel":
        login()
    elif set_uname.lower() == "n" or set_uname.lower() == "no":
        p_user = click.prompt(f'\nPlease type your desired username.\n')
        e_user = session.query(User).filter(User.username == p_user).first()

        while e_user:
            click.echo(f"\n{p_user} is already taken. Please try again. ")
            p_user = click.prompt(f'\nPlease type your desired username.\n')
            e_user = session.query(User).filter(User.username == p_user).first()


        p_email = click.prompt(f'\nPlease add your email address or hit "enter" to add it later.\n', default="")
        if p_email:
            while ("@" and "." not in p_email) or (p_email == True):
                p_email = click.prompt('\nInvalid email format. Please input a valid email address or press "enter" to skip.\n')

        p_region = click.prompt(f'\nPlease add your region as either "US", "EU", "JP" or hit "enter" to add it later. \n', default="")
        if p_region:
            while (p_region not in region) or (p_region == True):
                p_region = click.prompt('\nInvalid region. Please input "US", "EU", "JP" or press "enter" to skip.\n')

        p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
        c_password = click.prompt(f'Please confirm password', hide_input=True)

        p_match = True if c_password == p_password else False

        while not p_match:
            click.echo("\nPasswords did not match. Please try again.")
            p_password = click.prompt(f'\nPlease enter a password', hide_input=True)
            c_password = click.prompt(f'\nPlease confirm password', hide_input=True)

        new_user = User(username=p_user, email=p_email, region=p_region, password=p_password)

        confirm = click.prompt(f'\nIs this information correct?\n\nUsername: {p_user}, Email: {p_email}, Region: {p_region}\n\nType "confirm" if it is correct to submit registration. Type "no" to input information again.\n')

        if confirm.lower() == "confirm":
            session.add(new_user)
            session.commit()

            click.echo(f'\n{new_user} has been successfully registered. Please log in.\n')
            ctx.invoke(login, uname=p_user)
        else:
            ctx.invoke(register, uname=uname) 

    else:
        click.echo("\nInvalid input. Please try again.")
        ctx.invoke(register, uname=uname)

@cli.command()
@click.option('--user')
@click.pass_context
def search(ctx, user):
    choice = click.prompt('\nHow would you like to search? \n Type "title" to search by title. \n Type "platform" to search by platform. \n Type "genre" to search by genre. \n Type "price" to search by price. \n Type "back" to return to the Main menu. \n')

    if choice.lower() == "title":
        qtitle = click.prompt("\nPlease input the title keyword.\nQuery")
        result = [game for game in user.games if qtitle.lower() in game.title.lower()]
        
        if result:
            for game in result:
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice.lower() == "platform":
        qplat = click.prompt("\nPlease choose from the following platforms: \n PC, Switch, Xbox, Playstation. \nQuery")
        result = [game for game in user.games if qplat.lower() in game.platform.lower()]

        if result:
            for game in result:
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)  
    elif choice.lower() == "genre":
        qgenre = click.prompt("\nPlease choose from the following genres: \n FPS, RPG, Adventure, Strategy, MOBA. \nQuery")
        result = [game for game in user.games if qgenre.lower() in game.genre.lower()]

        if result:
            for game in result:
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice.lower() == "price":
        qprice = click.prompt("\nPlease input price as an integer. \nQuery")
        result = [game for game in user.games if int(qprice) == game.price]

        if result:
            for game in result:
                click.echo(f"\n{game}")
            ctx.invoke(search, user=user)
        else:
            click.echo("\nNo match found.")
            ctx.invoke(search, user=user)
    elif choice.lower() == "back" or choice.lower() == "..":
        ctx.invoke(main, user=user)
    else:
        click.echo("\nInput is not a valid option. Please try again.")
        ctx.invoke(main, user=user)

@cli.command()
@click.option('--user')
@click.pass_context
def main(ctx, user):
    """Main Menu"""

    choice = click.prompt('\nMAIN MENU:\n\nWhat would you like to do? \n Type "games" to view your library. \n Type "search" to search your library. \n Type "info" to view or edit your account info. \n Type "exit" to exit the application.\n')

    if choice.lower() == "games":
        ctx.invoke(library, user=user)
    elif choice.lower() == "info":
        ctx.invoke(account, user=user)              
    elif choice.lower() == "search":
        ctx.invoke(search, user=user)
    elif choice.lower() == "exit":
        click.echo("\n See you next time. \n")
        exit()
    else:
        click.echo("\nInput is not a valid option. Please try again")
        ctx.invoke(main, user=user)
    


@cli.command()
@click.option('--uname', prompt='\nWelcome to Game DB. Please input your username.\n\nUsername',
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

        if reg_prompt.lower() == "y" or reg_prompt.lower() == "yes":
            ctx.invoke(register, uname=uname)
        else:
            login() 



if __name__ == '__main__':
    
    login()
    


    