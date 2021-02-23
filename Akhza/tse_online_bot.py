
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
import urllib.request as urllib2
from urllib.parse import unquote, quote
from getDataFromTse import OnlineData
token = "322075834:AAFvIsmlahXjkXBSd6XXzYN4ebQpWTMysA8"
update_id = 0
state = 0
chat_id = 0
data = []
results = []
temp = ""
s = ""
obj = OnlineData()
start_flag = False


def main():
    global obj, temp, s
    """Run the bot."""
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
            if start_flag:
                while True:
                    s = obj.run()
                    if s != temp:
                        temp = s
                        bot.send_message(chat_id, str(s))
                        # urllib2.urlopen(
                        #     "https://api.telegram.org/bot"+token+"/sendMessage?chat_id=-1001154150516&text="+quote(s))
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id, state, chat_id, start_flag, runner_flag, s, results, obj
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            chat_id = update.message.chat.id
            print(update)
            print("\n\n\n")
            if(update.message.text == '/menu' or update.message.text == '/start'):
                obj.start()
                start_flag = True
                update.message.reply_text("""Welcome to Akhza Signal Bot
            """)


if __name__ == '__main__':
    main()
