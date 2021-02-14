import telepot
import time
import logging
from pprint import pprint
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
# from telepot.delegate import per_chat_id, create_open, pave_event_space
from telepot.loop import MessageLoop
from obj import *
import telegram
from telegram.error import NetworkError, Unauthorized
logging.basicConfig(filename='output.log', level=logging.INFO)
obj_archive = {}
state = 0
flag_rec = False
chat = 0
filter_list = []
filter_name = []
d = []
mana = []


def handler(msg):
    global state, filter_list, filter_name, flag_rec, chat, obj_archive, mana, d
    count = 0
    content_type, chat_type, chat_id = telepot.glance(msg)
    chat = chat_id
    print(content_type, chat_type, chat_id, msg['text'])
    if content_type == 'text':
        logging.info(msg['text'])

        if msg['text'] == '/menu':

            bot.sendMessage(chat_id, """لطفا یکی از گزینه های زیر را وارد کنید:
    /rec گرفتن اطلاعات
    /clear پاک کردن اطلاعات تا آن لحظه
    /add اضافه کردن فیلتر
    /admin ارتباط با ادمین
    /list لیست فیلتر ها
    /status آخرین وضعیت اطلاعات فیلتر شده
    /reset شروع دوباره با اضافه کردن فیلتر ها
    /stop توقف فرآیند
    /remove حذف فیلتر""", reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="/menu")],[KeyboardButton(text="/add")],[KeyboardButton(text="/rec")],
                    [KeyboardButton(text="/clear")]
                ]))
        elif msg['text'] == '/stop':
            if flag_rec:
                flag_rec = False
            else:
                bot.sendMessage(chat_id, 'فرآیندی هنوز فعال نیست')
        elif msg['text'] == '/remove':
            if len(filter_list) > 0:
                state = 100
                bot.sendMessage(
                    chat_id, 'لطفا نام فیلتر مورد نظر جهت حذف را وارد کنید.')
            else:
                bot.sendMessage(chat_id, 'هنوز فیلتری وارد نشده است.')
        elif state == 100:
            if msg['text'] in filter_name:
                index = filter_name.index(msg['text'])
                filter_name.pop(index)
                filter_list.pop(index)
                bot.sendMessage(chat_id, 'فیلتر شما با موفقیت حذف شد.')
                if flag_rec and len(filter_name) > 0:
                    obj_archive[chat_id].close()
                    del(obj_archive[chat_id])
                    obj_archive[chat_id] = fetch_data(filter_list, filter_name)
                    obj_archive[chat_id].initiate_page()
                    mana, d = obj_archive[chat_id].check()

                    # s=''
                    # for i in range(len(d)):
                    #     s+='اطلاعات {0}'.format(filter_name[i])
                    #     s+='\n'
                    #     for p in d[i]:
                    #         s+=p['namad']
                    #         s+='\t'
                    #         s+=p['price']
                    #         s+='\n'
                    #     s+='------------------------------------\n'
                    # bot.sendMessage(chat_id,s)
                    flag_rec = True
                else:
                    pass
                state = 0
            else:
                bot.sendMessage(
                    chat_id, 'فیلتری با این نام پیدا نشد برای شروع مجدد /menu را وارد کنید.')
        elif msg['text'] == '/admin':
            bot.sendMessage(chat_id, 'لطفا به ایدی @ali_raie پیام دهید')
        elif msg['text'] == '/status':
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

        elif msg['text'] == '/rec':
            if len(filter_list) > 0 and len(filter_name) > 0:
                s = fetch_data(filter_list, filter_name)
                s.initiate_page()
                mana, d = s.check()
                obj_archive[chat_id] = s
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
                bot.sendMessage(chat_id, s)
                flag_rec = True
            else:
                bot.sendMessage(
                    chat_id, 'فیلتری وارد نشده ابتدا فیلترهای خود را وارد کنید.')

        elif msg['text'] == '/clear':
            s = ''
        elif msg['text'] == '/reset':
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
                bot.sendMessage(chat_id, 'شما هنوز فرآیندی را آغاز نکرده اید.')
        elif msg['text'] == '/add':
            bot.sendMessage(
                chat_id, 'لطفا نام فیلتر مورد نظر خود را وارد کنید.')
            state += 1
        elif state == 1:
            filter_name.append(msg['text'])
            bot.sendMessage(chat_id, 'لطفا فیلتر خود را وارد کنید.')
            state += 1
        elif state == 2:
            filter_list.append(msg['text'])
            bot.sendMessage(chat_id, "مقادیر شما با موفقیت ثبت شد.")
            state = 0
        elif msg['text'] == '/list':
            if len(filter_list) != 0:
                bot.sendMessage(chat_id, str(filter_list))
            else:
                bot.sendMessage(chat_id, 'فیلتری وارد نشده است.')


# bot=telepot.Bot('1f19c5aa7e336684fbfc5bc1c4ea3d2dcbcf3999')
# bot=telepot.Bot('180560326:0973896afee515a1a79221cf99af569701dab7f0')
# bot = telepot.Bot('1321400315:AAE_IyobV6xI5iDLKmJxOmn_mPC9-pBFqqI')
# bot = telepot.Bot('407426760:AAEMxA_CDDg0Xox_iG-BBM_uKEkFCwf0fj0')

bot = telepot.Bot(token='1416825174:54aaafef3ee0d6412d9ee227aab70c02facf7476',
                        base_url="https:‎//tapi.bale.ai/")
# bot.getMe()
MessageLoop(bot, handler).run_as_thread()
# print(bot.getMe())
print('Listening ...')

# Keep the program running.
while 1:
    if flag_rec == True:
        try:
            na, da = obj_archive[chat].check()
            print(na)
            print(da)
            logging.info(str(na)+str(da))
            if da != d:
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
                bot.sendMessage(chat, s)

        except:
            pass

    time.sleep(0.2)
