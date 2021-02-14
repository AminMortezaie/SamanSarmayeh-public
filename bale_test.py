#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
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

channel_chat_id = "-1001339332906"
token = "1530708483:AAHSLPjr9qI09hhj5tIqb_-CdyYE3PC7Zag"  # gheir_hayoola_bot
amin_chat_id = 1405117927
group_id = 6367957794
update_id = 0
filter_name = []
filter_list = []
state = 0
obj_archive = {}
d = []
mana = []
flag_rec = False
chat_id = 0
path = 'filters'
entries = os.listdir(path)

for entry in entries:
    filter_name.append(entry.split(".txt")[0])

for name in filter_name:
    name_of_file = name+".txt"
    completeName = os.path.join(path, name_of_file)
    filter1 = open(completeName, 'r')
    filter_list.append(filter1.read())


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
    global update_id, d, filter_list, path

    # Telegram Bot Authorization Token
    bot = telegram.Bot(token)

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
                echo(bot)
                sleep(2)
                if flag_rec == True:
                    na, da = obj_archive[chat_id].check()
                    logging.info(str(na)+str(da))
                    if comperator(da) != comperator(d):
                        s = ''
                        for i in range(len(da)):
                            s += 'اطلاعات {0}'.format(filter_name[i])
                            s += '\n'
                            for d in da[i]:
                                s += d['namad']
                                s += '\t'
                                s += d['price']
                                s += '\n'
                            s += '------------------------------------\n'
                        d = da[:]
                        mana = na[:]
                        bot.send_message(chat_id, s)
                        urllib2.urlopen(
                            "https://api.telegram.org/bot"+token+"/sendMessage?chat_id=-1001339332906&text="+quote(s))

            except NetworkError:
                sleep(1)
            except Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id, state, filter_list, filter_name, flag_rec, obj_archive, mana, d, chat_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            chat_id = update.message.chat.id
            print(update)
            if(update.message.text == '/menu'):
                update.message.reply_text("""لطفا یکی از گزینه های زیر را وارد کنید:
            /rec گرفتن اطلاعات
            /clear پاک کردن اطلاعات تا آن لحظه
            /add اضافه کردن فیلتر
            /list لیست فیلتر ها
            /status آخرین وضعیت اطلاعات فیلتر شده
            /reset شروع دوباره با اضافه کردن فیلتر ها
            /stop توقف فرآیند
            /remove حذف فیلتر""")

            if(update.message.text == '/add'):
                update.message.reply_text(
                    'لطفا نام فیلتر مورد نظر خود را وارد کنید.')
                update.message.reply_text(str(state))
                state += 1
                update.message.reply_text(str(state))
            elif(state == 1):
                filter_name.append(update.message.text)
                update.message.reply_text('لطفا فیلتر خود را وارد کنید.')
                state += 1
            elif(state == 2):
                filter_list.append(update.message.text)
                update.message.reply_text("مقادیر شما با موفقیت ثبت شد.")
                state = 0

            elif update.message.text == '/cancel':
                state = 0
                update.message.reply_text("فرایند کنسل شد.")

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
                    bot.sendMessage(chat_id, "برای شروع /menu را وارد کنید.")
                else:
                    bot.sendMessage(
                        chat_id, 'شما هنوز فرآیندی را آغاز نکرده اید.')

            elif update.message.text == '/remove':
                if len(filter_list) > 0:
                    state = 100
                    bot.sendMessage(
                        chat_id, 'لطفا نام فیلتر مورد نظر جهت حذف را وارد کنید.')
                else:
                    bot.sendMessage(chat_id, 'هنوز فیلتری وارد نشده است.')
            elif state == 100:
                if update.message.text in filter_name:
                    index = filter_name.index(update.message.text)
                    filter_name.pop(index)
                    filter_list.pop(index)
                    bot.sendMessage(chat_id, 'فیلتر شما با موفقیت حذف شد.')
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
                        chat_id, 'فیلتری با این نام پیدا نشد برای شروع مجدد /menu را وارد کنید.')

            elif update.message.text == '/status':
                s = ''
                if flag_rec:
                    for i in range(len(d)):
                        s += 'اطلاعات {0}'.format(filter_name[i])
                        s += '\n'
                        for p in d[i]:
                            s += p['namad']
                            s += '\t'
                            s += p['price']
                            s += '\n'
                        s += '------------------------------------\n'
                    bot.sendMessage(chat_id, s)
                else:
                    s = 'هنوز /rec فعال نشده است'
                    bot.sendMessage(chat_id, s)

            elif update.message.text == '/list':
                if len(filter_name) != 0:
                    update.message.reply_text(str(filter_name))
                else:
                    update.message.reply_text('فیلتری وارد نشده است.')
            elif update.message.text == '/stop':
                flag_rec = False
            elif update.message.text == '/clear':
                s = ''
                update.message.reply_text('مقادیر با موفقیت حذف شد.')
            elif update.message.text == '/rec':
                update.message.reply_text('دیتا در حال بارگیری میباشد...')
                if len(filter_list) > 0 and len(filter_name) > 0:
                    s = fetch_data(filter_list, filter_name)
                    s.initiate_page()
                    mana, d = s.check()
                    print("mana:   "+str(mana)+"\n\n\n\n\n\n")
                    print("d:   "+str(d)+"\n\n\n\n\n\n")
                    obj_archive[chat_id] = s
                    print("obj------"+str(obj_archive)+"\n\n\n\n\n\n\n")
                    s = ''
                    for i in range(len(d)):
                        s += 'اطلاعات {0}'.format(filter_name[i])
                        s += '\n'
                        for p in d[i]:
                            s += p['namad']
                            s += '\t'
                            s += p['price']
                            s += '\n'
                        s += '------------------------------------\n'
                    update.message.reply_text(s)
                    urllib2.urlopen(
                        "https://api.telegram.org/bot"+token+"/sendMessage?chat_id=-1001339332906&text="+quote(s))
                    flag_rec = True
                else:
                    update.message.reply_text(
                        'فیلتری وارد نشده ابتدا فیلترهای خود را وارد کنید.')


if __name__ == '__main__':
    main()
