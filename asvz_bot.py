#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

base_url = ""

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('welcome to ASVZ BOT!')
    # TODO: Add how to text and usage of bot


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def kondi(bot, update):
    """return the next 5 kondis"""
    req = requests.get('{0}Lessons?SportId=82&Skip=0&Take=5'.format(base_url))
    if req.status_code == 200:
        data = json.loads(req.content.decode('utf-8'))
    else:
        logger.error("no response from asvz api")
        return -1
    response = "next 5 kondis:\n"
    for e in data:
        response += '{0}\n{1}\n{2}\n'.format(e['fromDateTime'], e['location']['de'], e['title']['de'])
    update.message.reply_text(response)



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    global base_url
     # load the config file
    with open('config.json') as config_file:
        config = json.load(config_file)

    base_url = config['asvz_api']    
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['telegram_token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("kondi", kondi))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
