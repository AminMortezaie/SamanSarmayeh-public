

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""

from persiantools.jdatetime import JalaliDate
import datetime
import time
import json
from datetime import date
import datetime
import logging
from time import sleep
from obj import *
import telegram
from telegram.error import NetworkError, Unauthorized
import os
import urllib.request as urllib2
from urllib.parse import unquote, quote
import datetime
from datetime import datetime as r

# token = "53284502:3ae2b7dacc94b0b18209105ed933c8197e1898d9"
token_telegram = "1372017525:AAEWmLm0ZB0hWpzvVY74S0vN4eeaqH68I6o"
channel_chat_id = "-1001209131813"
amin_chat_id = 1405117927
rahimi_chat_id = 1627417803
update_id = 0
filter_name = []
filter_list = []
state = 0
obj_archive = {}
d = []
mana = []
flag_rec = False
chat_id = 0
path = 'hayoola'
entries = os.listdir(path)
buy_list_plus = []  # 3
buy_list_bache = []  # 0
buy_list_eslah = []  # 1
login_flag = False

bought_stocks = []

for entry in entries:
    filter_name.append(entry.split(".txt")[0])

for name in filter_name:
    name_of_file = name+".txt"
    completeName = os.path.join(path, name_of_file)
    filter1 = open(completeName, 'r')
    filter_list.append(filter1.read())

def writeOnFile(date, array):
    path = 'history/hayoola'
    name_of_file = "Hayoola_"+str(date)+".txt"
    completeName = os.path.join(path, name_of_file)
    file1 = open(completeName, 'a',encoding="UTF-8")
    file1.write("\n")
    file1.write(array)

def comperator(d):
    lst = []
    for i in range(len(d)):
        temp = []
        for j in range(len(d[i])):
            temp.append(d[i][j]['namad'])
        lst.append(temp)
    return lst


def main():
    """Run the bot."""
    global update_id, d, filter_list, path, login_flag, bought_stocks

    # Telegram Bot Authorization Token
    # bot = telegram.Bot(token=token,
    #                    base_url="https://tapi.bale.ai/")

    bot = telegram.Bot(token=token_telegram)

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
        if str(datetime.time(9, 5, 0)) < r.now().strftime("%H:%M:%S") < str(datetime.time(12, 30, 0)):
            try:
                # if(not login_flag):
                #     obj_archive[chat_id].login()
                #     login_flag = True
                echo(bot)
                sleep(2)
                if flag_rec == True:
                    na, da = obj_archive[chat_id].check()
                    logging.info(str(na)+str(da))
                    if comperator(da) != comperator(d):
                        s = ''
                        buy_list_plus = []  # 3
                        buy_list_bache = []  # 0
                        buy_list_eslah = []  # 1

                        for i in range(len(da)):
                            s += '?????????????? {0}'.format(filter_name[i])
                            s += '\n'
                            for d in da[i]:
                                if(i == 0):
                                    buy_list_bache.append(
                                        [d['namad'], d['price']])
                                if(i == 1):
                                    buy_list_eslah.append(
                                        [d['namad'], d['price']])
                                if(i == 3):
                                    buy_list_plus.append(
                                        [d['namad'], d['price']])
                                s += d['namad']
                                s += '\t'
                                s += d['price']
                                s += '\n'
                            s += '------------------------------------\n'
                        writeOnFile(JalaliDate.today(), s)
                        print("bache: ", str(buy_list_bache))
                        print("eslah: ", str(buy_list_eslah))
                        print('plus: ', str(buy_list_plus))

                        # if(len(buy_list_plus) != 0):
                        #     for order in buy_list_plus:
                        #         if (order[0] not in bought_stocks):
                        #             obj_archive[chat_id].searchNamad(order[0])
                        #             obj_archive[chat_id].orderBuy(
                        #                 order[1], 00000000)
                        #             bought_stocks.append(order[0])

                        # if(len(buy_list_bache) != 0):
                        #     for order in buy_list_bache:
                        #         if (order[0] not in bought_stocks):
                        #             obj_archive[chat_id].searchNamad(order[0])
                        #             obj_archive[chat_id].orderBuy(
                        #                 order[1], 00000000)
                        #             bought_stocks.append(order[0])

                        # if(len(buy_list_eslah) != 0):
                        #     for order in buy_list_eslah:
                        #         if (order[0] not in bought_stocks):
                        #             obj_archive[chat_id].searchNamad(order[0])
                        #             obj_archive[chat_id].orderBuy(
                        #                 order[1], 00000000)
                        #             bought_stocks.append(order[0])

                        d = da[:]
                        mana = na[:]
                        urllib2.urlopen(
                        "https://api.telegram.org/bot1372017525:AAEWmLm0ZB0hWpzvVY74S0vN4eeaqH68I6o/sendMessage?chat_id=-1001209131813&text="+quote(s))
                        bot.send_message(chat_id, s)
                    
                        # bot.send_message(amin_chat_id, s)
                        # bot.send_message(rahimi_chat_id,s)
            except NetworkError:
                sleep(1)
            except Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id, state, filter_list, filter_name, flag_rec, obj_archive, mana, d, chat_id, bought_stocks
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            chat_id = update.message.chat.id
            print(update)
            if(update.message.text == '/menu'):
                update.message.reply_text("""???????? ?????? ???? ?????????? ?????? ?????? ???? ???????? ????????:
            /rec ?????????? ??????????????
            /clear ?????? ???????? ?????????????? ???? ???? ????????
            /add ?????????? ???????? ??????????
            /list ???????? ?????????? ????
            /status ?????????? ?????????? ?????????????? ?????????? ??????
            /reset ???????? ???????????? ???? ?????????? ???????? ?????????? ????
            /stop ???????? ????????????
            /remove ?????? ??????????""")

            if(update.message.text == '/add'):
                update.message.reply_text(
                    '???????? ?????? ?????????? ???????? ?????? ?????? ???? ???????? ????????.')
                update.message.reply_text(str(state))
                state += 1
                update.message.reply_text(str(state))
            elif(state == 1):
                filter_name.append(update.message.text)
                update.message.reply_text('???????? ?????????? ?????? ???? ???????? ????????.')
                state += 1
            elif(state == 2):
                filter_list.append(update.message.text)
                update.message.reply_text("???????????? ?????? ???? ???????????? ?????? ????.")
                state = 0

            elif update.message.text == '/cancel':
                state = 0
                update.message.reply_text("???????????? ???????? ????.")

            elif update.message.text == '/reset':
                if flag_rec:
                    d = []
                    mana = []
                    filter_list = []
                    filter_name = []
                    obj_archive[chat_id].close()
                    obj_archive.pop(chat_id)
                    flag_rec = False
                    print(flag_rec)
                    bot.sendMessage(chat_id, "???????? ???????? /menu ???? ???????? ????????.")
                else:
                    bot.sendMessage(
                        chat_id, '?????? ???????? ?????????????? ???? ???????? ?????????? ??????.')

            elif update.message.text == '/remove':
                if len(filter_list) > 0:
                    state = 100
                    bot.sendMessage(
                        chat_id, '???????? ?????? ?????????? ???????? ?????? ?????? ?????? ???? ???????? ????????.')
                else:
                    bot.sendMessage(chat_id, '???????? ???????????? ???????? ???????? ??????.')
            elif state == 100:
                if update.message.text in filter_name:
                    index = filter_name.index(update.message.text)
                    filter_name.pop(index)
                    filter_list.pop(index)
                    bot.sendMessage(chat_id, '?????????? ?????? ???? ???????????? ?????? ????.')
                    if flag_rec and len(filter_name) > 0:
                        obj_archive[chat_id].close()
                        del(obj_archive[chat_id])
                        obj_archive[chat_id] = fetch_data(
                            filter_list, filter_name)
                        obj_archive[chat_id].initiate_page()
                        mana, d = obj_archive[chat_id].check()
                        flag_rec = True

                    else:
                        pass
                    state = 0
                else:
                    bot.sendMessage(
                        chat_id, '???????????? ???? ?????? ?????? ???????? ?????? ???????? ???????? ???????? /menu ???? ???????? ????????.')

            elif update.message.text == '/status':
                s = ''
                if flag_rec:
                    for i in range(len(d)):
                        s += '?????????????? {0}'.format(filter_name[i])
                        s += '\n'
                        for p in d[i]:
                            s += p['namad']
                            s += '\t'
                            s += p['price']
                            s += '\n'
                        s += '------------------------------------\n'

                    bot.sendMessage(chat_id, s)
                else:
                    s = '???????? /rec ???????? ???????? ??????'
                    bot.sendMessage(chat_id, s)

            elif update.message.text == '/list':
                if len(filter_name) != 0:
                    update.message.reply_text(str(filter_name))
                else:
                    update.message.reply_text('???????????? ???????? ???????? ??????.')
            elif update.message.text == '/stop':
                flag_rec = False
                update.message.reply_text('???????? ???? ???????????? ?????????? ????.')
            elif update.message.text == '/clear':
                s = ''
                update.message.reply_text('???????????? ???? ???????????? ?????? ????.')

            # rec
            # function

            elif update.message.text == '/rec':
                update.message.reply_text('???????? ???? ?????? ?????????????? ????????????...')

                if len(filter_list) > 0 and len(filter_name) > 0:
                    s = fetch_data(filter_list, filter_name)
                    s.initiate_page()
                    mana, d = s.check()
                    obj_archive[chat_id] = s
                    # obj_archive[chat_id].login()
                    s = ''
                    for i in range(len(d)):
                        s += '?????????????? {0}'.format(filter_name[i])
                        s += '\n'
                        for p in d[i]:
                            if(i == 0):
                                buy_list_bache.append(
                                    [p['namad'], p['price']])
                            if(i == 1):
                                buy_list_eslah.append(
                                    [p['namad'], p['price']])
                            if(i == 3):
                                buy_list_plus.append(
                                    [p['namad'], p['price']])
                            s += p['namad']
                            s += '\t'
                            s += p['price']
                            s += '\n'
                        s += '------------------------------------\n'
                    writeOnFile(JalaliDate.today(), s)
                    print("bache: ", str(buy_list_bache))
                    print("eslah: ", str(buy_list_eslah))
                    print('plus: ', str(buy_list_plus))

                    # if(len(buy_list_plus) != 0):
                    #     for order in buy_list_plus:
                    #         if (order[0] not in bought_stocks):
                    #             obj_archive[chat_id].searchNamad(order[0])
                    #             obj_archive[chat_id].orderBuy(
                    #                 order[1], 300000000)
                    #             bought_stocks.append(order[0])
                    #             print(bought_stocks)

                    # if(len(buy_list_bache) != 0):
                    #     for order in buy_list_bache:
                    #         if (order[0] not in bought_stocks):
                    #             obj_archive[chat_id].searchNamad(order[0])
                    #             obj_archive[chat_id].orderBuy(
                    #                 order[1], 200000000)
                    #             bought_stocks.append(order[0])
                    #             print(bought_stocks)

                    # if(len(buy_list_eslah) != 0):
                    #     for order in buy_list_eslah:
                    #         if (order[0] not in bought_stocks):
                    #             obj_archive[chat_id].searchNamad(order[0])
                    #             obj_archive[chat_id].orderBuy(
                    #                 order[1], 100000000)
                    #             bought_stocks.append(order[0])
                    #             print(bought_stocks)

                    urllib2.urlopen(
                    "https://api.telegram.org/bot1372017525:AAEWmLm0ZB0hWpzvVY74S0vN4eeaqH68I6o/sendMessage?chat_id=-1001209131813&text="+quote(s))
                    update.message.reply_text(s)
                    flag_rec = True
                else:
                    update.message.reply_text(
                        '???????????? ???????? ???????? ?????????? ???????????????? ?????? ???? ???????? ????????.')


if __name__ == '__main__':
    main()
