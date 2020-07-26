#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

TOKEN=""
kindle_email=""

config_keyboard = [['Kindle email'],
                  ['Personal email'],
                  ['Done']]
config_markup = ReplyKeyboardMarkup(config_keyboard, one_time_keyboard=True)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
CONFIG_BASE, CONFIG_KINDLE_EMAIL, CONFIG_USER_EMAIL = range(3)

with open(".secret", 'r') as f:
    TOKEN=f.readline()

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Send me Web URLs, I\'ll send a kindle-friendly PDF to your kindle.')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send me Web URLs, I\'ll send a kindle-friendly PDF to your kindle.')


def config_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Which setting do you want to change?', reply_markup=config_markup)
    return CONFIG_BASE

def config_kindle_email(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Write me your Kindle\'s email address')
    return CONFIG_KINDLE_EMAIL

def config_user_email(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Log in with your Gmail account.')
    return CONFIG_USER_EMAIL

def done(update, context):
    update.message.reply_text("Settings ok")

    return ConversationHandler.END


def from_url(update, context):
    """Convert a web page to a kindle-friendly PDF, than send it to the device's email"""
    context.sendChatAction('upload_document')
    update.message.reply_text("Sending page to kindle")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('config', config_command)],

        states={
            CONFIG_BASE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Kindle email$')),
                               config_kindle_email),
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Personal email$')),
                               config_user_email)
            ],

            CONFIG_KINDLE_EMAIL: [
                ],

            CONFIG_USER_EMAIL: [
                ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )
    dp.add_handler(conv_handler)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, from_url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()