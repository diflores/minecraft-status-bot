# Minecraft Status Bot

## About

This Telegram bot is able to retrieve useful information about a given Minecraft Server. Built with Python 3.7.

## SETUP

Before running the bot, you need to define its credentials in a `.env` file:

```
MINECRAFT_SERVER_IP=
MINECRAFT_SERVER_PORT=
TELEGRAM_BOT_TOKEN=
NEW_PLAYERS_CHAT_ID=
```

The bot is intended for using with Poetry, by running the following commands:

1. Install Poetry:

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

2. Install requirements with: `poetry install`.

## How to run

```
$ poetry shell
$ python bot.py
```


## How to use

Add your bot to a group and use the following commands:

```
/start Starts the bot.
/players_online Retrieves players currently online.
/server_status Checks if server is online.
/pucha Sends a Cries in Spanish GIF.
```

The bot checks every 60 seconds if there are new players online. If so, sends a mesage to the chat with id `NEW_PLAYERS_CHAT_ID`, with a list of those new players. 

## TO-DO

- Add a DBMS to store chat ids and list of online players.
- Find a more elegant way to alert when new players are online.


## Credits

This bot wouldn't have been possible without the following resources:

- https://api.mcsrvstat.us/
- https://github.com/Dinnerbone/mcstatus
