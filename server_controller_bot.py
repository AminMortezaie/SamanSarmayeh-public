
from persiantools.jdatetime import JalaliDate
import datetime

import time
import json
from datetime import date
import datetime
from time import sleep
import telegram
from telegram.error import NetworkError, Unauthorized
import os
from server_controller import *

token = "1512492218:AAH6tBiijJ_l12MBN260v5Hwh9-GtTtEjak"  # server_controller1_bot
update_id = 0
state = 0
chat_id = 0


def main():
    """Run the bot."""
    global update_id, temp, start_flag, runner_flag

    # Telegram Bot Authorization Token
    bot = telegram.Bot(token=token)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        bot.delete_webhook()
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    # Enable logging
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                     level=logging.DEBUG)

    while True:
        try:
            echo(bot)
            sleep(2)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id, state, chat_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            chat_id = update.message.chat.id
            print(str(update)+"\n\n\n")

            if(update.message.text == '/help' or update.message.text == '/start'):
                update.message.reply_text("""
                commands:
                /start_service
                /stop_service


                1--> hayoola
                2--> non hayoola
                3--> dastkari 0
                5--> dastkari 1
                6--> dastkari 2
                7--> dastkari_test
                """)
           

            if(update.message.text == '/start_service'):
                update.message.reply_text("Send your service name to START.")
                state = 1
            elif(state == 1):
                try:
                    ServerController().start_program(update.message.text)
                    update.message.reply_text("Service started successfully!")
                    state = 0
                except:
                    update.message.reply_text("Service starting failed!")
                    state = 0

            if(update.message.text == '/stop_service'):
                update.message.reply_text("Send your service name to STOP.")
                state = 10
            elif(state == 10):
                try:
                    ServerController().stop_program(update.message.text)
                    update.message.reply_text("Service stopped successfully!")
                    state = 0
                except:
                    update.message.reply_text("Service stopping failed!")
                    state = 0


if __name__ == '__main__':
    main()
