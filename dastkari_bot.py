
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
from dastkari_class import *
import urllib.request as urllib2
from urllib.parse import unquote, quote

token = "1565948803:AAFWxKXtA-tXPHaAWGyBG6kE-_lDNvXr92Y"
token_test = "308134655:AAFwp-dJyKf3Xn25ysa_0mA_ChhR07c0BgI"
update_id = 0
state = 0
chat_id = 0
namad_list = []
namad_list_seen = []
data = []
results = []
start_flag = False
runner_flag = False
temp = ""
s = ""


def makeObj():
    if namad_list:
        for namad in namad_list:
            if namad not in namad_list_seen:
                data.append((namad, FindDastkari(namad)))
                namad_list_seen.append(namad)
        startProcess()
        return True
    else:
        return False


def startProcess():
    global results
    results = []
    for obj in data:
        results.append([obj[0], obj[1].run()])


def startRunner():
    global results
    results = []
    for obj in data:
        results.append([obj[0], obj[1].runner()])


def addWatchListToNamads():
    global namad_list
    f = open("watch_list.txt", encoding="utf-8", mode="r")
    for line in f.readlines():
        namad_list.append(line.split("\n")[0])


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
            if start_flag:
                if len(results) > 0:
                    s = ""
                    for result in results:
                        s += " نماد " + \
                            result[0]+" :" + "\n"+result[1]+"\n\n\n"
                    if s != temp:
                        bot.send_message(chat_id, s)
                        urllib2.urlopen(
                            "https://api.telegram.org/bot"+token_test+"/sendMessage?chat_id=-1001154150516&text="+quote(s))
                        temp = s
            if runner_flag:
                startRunner()
                if results:
                    s = ""
                    for result in results:
                        s += " نماد " + \
                            result[0]+" :" + "\n"+result[1]+"\n\n\n"
                    if s != temp:
                        bot.send_message(chat_id, s)
                        urllib2.urlopen(
                            "https://api.telegram.org/bot"+token_test+"/sendMessage?chat_id=-1001154150516&text="+quote(s))
                        temp = s
                start_flag = False
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id, state, chat_id, start_flag, runner_flag, s, results
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            chat_id = update.message.chat.id
            print(update)
            print("\n\n\n")
            if(update.message.text == '/menu' or update.message.text == '/start'):
                update.message.reply_text("""لطفا یکی از گزینه های زیر را وارد کنید:
            /help دریافت اطلاعات مربوط به ربات
            /add ورود نام سهم
            /list دیدن نام سهام ها
            /run بررسی یکباره سهم
            /runner بررسی مداوم سهم
            /menu دیدن منو
            """)

            if(update.message.text == '/help'):
                update.message.reply_text(
                    """این ربات برای بررسی دستکاری در سهم ها می باشد.
ابتدا نام نماد های مورد نظر را به کمک /add به طور کامل وارد کنید سپس با ارسال /run ربات را اجرا کنید.
در صورت تمایل برای بررسی پیاپی سهم از /runner استفاده کنید.
پاک کردن یک سهم خاص /remove
اضافه کردن واچ لیست از دستور /watch                             
                     """)

            if(update.message.text == '/watch'):
                addWatchListToNamads()
                update.message.reply_text("واچ لیست با موفقیت اضافه شد.")

            if(update.message.text == '/add'):
                start_flag = False
                update.message.reply_text("سهم مورد نظر را وارد کنید.")
                state += 1
            elif(state == 1):
                if update.message.text not in namad_list:
                    namad_list.append(update.message.text)
                    update.message.reply_text(
                        "سهم "+"\""+update.message.text+"\""+" با موفقیت افزوده شد.")
                else:
                    update.message.reply_text(
                        "سهم "+"\""+update.message.text+"\""+" تکراری میباشد لطفا یک سهم تازه وارد کنید.")

                state = 0

            if(update.message.text == '/remove'):
                update.message.reply_text("سهم مورد نظر را وارد کنید.")
                state += 10
            elif(state == 10):
                if update.message.text in namad_list:
                    namad_list.remove(update.message.text)
                    if update.message.text in namad_list_seen:
                        namad_list_seen.remove(update.message.text)
                    update.message.reply_text(
                        "سهم "+"\""+update.message.text+"\""+" با موفقیت حذف شد.")

                else:
                    update.message.reply_text(
                        "سهم "+"\""+update.message.text+"\""+" در بین نمادها وجود ندارد.")

                state = 0
            if(update.message.text == '/list'):
                if(namad_list):
                    update.message.reply_text(str(namad_list))
                else:
                    update.message.reply_text(
                        "سهمی وارد نشده است لطفا ابتدا سهمی را وارد کنید.")

            if(update.message.text == '/run'):
                if(not namad_list):
                    update.message.reply_text(
                        "سهمی وارد نشده است لطفا ابتدا سهمی را وارد کنید.")

                else:
                    update.message.reply_text(
                        "درخواست شما دریافت شد لطفا منتظر بمانید.. ")
                    update.message.reply_text("مود بررسی یکباره فعال شد.")

                    start_flag = True
                    if not makeObj():
                        update.message.reply_text(
                            "پروسه موفقیت آمیز نبود! دوباره تلاش کنید.")

            if(update.message.text == '/stop'):
                start_flag = False
                runner_flag = False
                s = ''
                results = []
                update.message.reply_text(
                    " فرآیند با موفقیت متوقف شد.")

            if(update.message.text == '/runner'):

                if(not namad_list):
                    update.message.reply_text(
                        "سهمی وارد نشده است لطفا ابتدا سهمی را وارد کنید.")

                else:
                    update.message.reply_text(
                        "درخواست شما دریافت شد لطفا منتظر بمانید.. ")
                    update.message.reply_text("مود بررسی پیاپی فعال شد.")
                    runner_flag = True
                    if not makeObj():
                        update.message.reply_text(
                            "پروسه موفقیت آمیز نبود! دوباره تلاش کنید.")


if __name__ == '__main__':
    main()
