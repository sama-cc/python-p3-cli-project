# Game DB

Game DB is a Command Line Interface(CLI) application that is designed to help you manage your game library using a database. 

## Description

The DB in Game DB stands for database.  Game DB is an easy-to-use application to manage your game library using the power and effciency of a SQL database without writing any SQL code! With it you can view your games, search for specific games in your library, and add or remove games.

## Installation

Simply download the Game DB folder. Navigate to the lib folder and double click on the game_db.py file. Alternatively you can open your terminal, navigate to the lib folder and run 'python3 game_db.py'.

## Usage

Game DB is straightforward to use. After logging in or registering you will be greeted with the Main Menu. Each menu in Game DB has clear instructions to help you navigate showing exactly what your options are. Other menus that are available that will be detailed further below are:

- Library Menu - View, add or remove games.

- Search Menu - Search for games with different filter options.

- Account Menu - View or edit your account information.

### Login

Below is what the login prompt looks like when you first run Game DB. If you are already registered you simply type your username and password.

```
Welcome to Game DB. Please input your username.

Username:

Password:
Confirm password:
```
### Register

If you are not registered typing your desired username will start the registration process.

```
Username: user_example

user_example is not in the list of registered usernames. Would you like to register now? y/n?:
```

If you do not want to use the username you initially typed you can instead type a different username. If the username is available you will then be prompted for additional account information.

```
Would you like to register as user_example? y/n? Type "cancel" to cancel:
```

You will be prompted for your email address and your region. You can click "enter" to skip to the next prompt. Below is an example.

```
Please add your email address or hit "enter" to add it later.
```

When you have gone through all of the registration prompts you will be asked to verify the information.

```
Is this information correct?

Username: user_example, Email: example@example.com, Region: US

Type "confirm" if it is correct to submit registration. Type "no" to input information again.
```

If registration was successful you will be greeted with the following message and will be prompted to log in with your password.

```
Username: "user_example", Email: "example@example.com", Region: "US", Joined: "2023-08-28 01:56:56" has been successfully registered. Please log in.
Password:
```

### Main Menu

Upon successful log in you will be greeted with the Main Menu at which you can navigate to the various sub-menus.

```
Welcome user_example. Loading your Game DB...

MAIN MENU:

What would you like to do?
 Type "games" to view your library.
 Type "search" to search your library.
 Type "info" to view or edit your account info.
 Type "exit" to exit the application.
```
### Library Menu

The Library Menu is where you go to do anything concerning your game library. There are many easy-to-understand options as shown below. 

```
LIBRARY MENU

What would you like to do with your game library?
 Type "all" to view all games in your library.
 Type "search" to search for a game in your library.
 Type "add" to add a game to your library.
 Type "remove" to remove a game from your library.
 Type "back" to return to the Main menu.
```
### Search Menu

As the name implies you can search through your game library at the Search Menu using different filter options listed below.

```
SEARCH MENU:

How would you like to search?
 Type "title" to search by title.
 Type "platform" to search by platform.
 Type "genre" to search by genre.
 Type "price" to search by price.
 Type "back" to return to the Main menu.
```
### Account Menu

The Account Menu is where you go to view your user information. You can make changes to your account if through the options listed below.

```
ACCOUNT MENU

Your account info:

Username: "user_example", Email: "example@example.com", Region: "US", Joined: "2023-08-28 01:56:56"

 Type "username" to change username.
 Type "email" to change email address.
 Type "region" to change region.
 Type "back" to go back to the previous menu.
```
## Debug

Administrative-like features can currently only be accessed through running 'debug.py'

There are two classes available. User and Game.

### Available User Methods:

#### Instance

- games_by_title() - Search a users games by title. Must provide string.
    

- games_by_price() - Search a users games by price. Must provide integer.
    

- games_by_platform() - Search a users games by platform. Must provide string.
    

- games_by_genre() - Search a users games by genre. Must provide string.


#### Class

- find_user() - Search for a user in the User table of the database. Must provide username string.  


- by_email() - Search for a user in the User table of the database by email. Must provide string.


- by_region() - Search for a user in the User table of the database by region. Must provide string US, EU, or JP.


- get_all() - Returns all users.
    

- print_all() - prints all users.


### Available Game Methods:

#### Instance

- users_by_username() - Returns all usernames for users that own the game. Must provide username string.
    

- users_by_region() - Returns all regions for users that own the game. Must provide string US, EU, or JP.


#### Class

- find_title() - Search for a game in the Game table of the database by game title. Must provide string.  


- by_price() - Search for a game in the Game table of the database by game price. Must provide integer.

- by_platform() - Search for a game in the Game table of the database by game platform. Must provide string PC, Xbox, Switch, Playstation.


- by_genre() - Search for a game in the Game table of the database by game genre. Must provide string FPS, RPG, Adventure, Strategy, MOBA.


- get_all() - Returns all games.
    

- print_all() - prints all games.

## Video Walkthrough

Follow the link below for a video walkthrough.

## FAQ

- Q. I noticed information that is innacurate. Can you please fix it?

    A. Please contact me using the email listed in the Support section.

- Q. I am experiencing a bug. Can I get help?

    A. Please contact me using the email listed in the Support section.

## Roadmap

- Allow an admin mode to view and manage all users in a database.
- Allow admin mode to add games to the catalogue.

## Support

If you have any questions regarding how Game DB is used or encounter any issues please feel free to contact me using the contact information below.

Email: sam.camhi@gmail.com

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## Credit

Below is a list of materials that I did not create and must give credit:

1. https://click.palletsprojects.com/en/8.1.x/ - Click was used to help create the CLI.

## License

[MIT](https://choosealicense.com/licenses/mit/)