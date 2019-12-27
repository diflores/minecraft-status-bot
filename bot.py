import os
import socket

from dotenv import load_dotenv
from mcstatus import MinecraftServer
from telegram import ParseMode
from telegram.ext import CallbackContext, CommandHandler, Updater

load_dotenv()

MINECRAFT_SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")
MINECRAFT_SERVER_PORT = int(os.getenv("MINECRAFT_SERVER_PORT"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NEW_PLAYERS_CHAT_ID = os.getenv("NEW_PLAYERS_CHAT_ID")

minecraft_server = MinecraftServer(MINECRAFT_SERVER_IP, MINECRAFT_SERVER_PORT)
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
updater_jobs = updater.job_queue


def start(update, context):
    """
        Replies to /start command.
    """
    print(f"Chat: {update.message.chat_id} started bot.")
    context.bot.send_message(chat_id=update.message.chat_id, text="¡Hola!")


def players_online(update, context):
    """
        Replies to /players_online command.
    """
    print(f"Chat: {update.message.chat_id} requested players online.")
    query = minecraft_server.query()
    current_players = query.players.names
    if current_players:
        players_online = current_players
        message = "Jugadores online:\n"
        for index, player in enumerate(players_online, 1):
            message += f"{index}. *{player}*\n"
    else:
        message = "No hay jugadores conectados."
    context.bot.send_message(
        chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN
        )


def server_status(update, context):
    """
        Replies to /server_status command.
    """
    print(f"Chat: {update.message.chat_id} requested server online.")
    try:
        status = minecraft_server.status()
        if status:
            message = "El servidor está *online*."
        else:
            message = "El servidor está *offline*."
    except socket.timeout:
        message = "El servidor está *offline*."
    finally:
        context.bot.send_message(
            chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN
            )


def callback_new_player(context: CallbackContext):
    """
        This function is called every 60 seconds to check whether there are
        new players online on our Minecraft server. If so, the bot sends a message to the
        chat with id NEW_PLAYERS_CHAT_ID with a list of the new players.
    """
    query = minecraft_server.query()
    current_players = query.players.names
    with open(".players") as f:  # Check file with previous online players
        old_players = f.readlines()
        old_players = [player.strip() for player in old_players]
    if len(current_players) > len(old_players):
        difference = list(set(current_players) - set(old_players))
        if len(difference) == 1:
            message = f"Nuevo jugador en línea:\n *{difference[0]}*"
        else:
            message = "Nuevos jugadores en línea:\n"
            for player in players_online:
                message += f"- *{player}*\n"
        context.bot.send_message(
            chat_id=NEW_PLAYERS_CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN
            )
    if current_players != old_players:
        with open(".players", "w") as f:  # Update players file if needed.
            for player in current_players:
                f.write(f"{player}\n")


def pucha(update, context):
    """
        Replies to /pucha command.
    """
    print(f"Chat: {update.message.chat_id} requested pucha GIF.")
    context.bot.send_animation(
        update.message.chat_id, "https://tenor.com/FzC5.gif",
        )


if __name__ == "__main__":
    start_handler = CommandHandler("start", start)
    players_online_handler = CommandHandler("players_online", players_online)
    server_status = CommandHandler("server_status", server_status)
    pucha = CommandHandler("pucha", pucha)
    updater_jobs.run_repeating(callback_new_player, interval=60, first=0)
    print("Bot is running.")
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(players_online_handler)
    dispatcher.add_handler(server_status)
    dispatcher.add_handler(pucha)
    updater.start_polling()
