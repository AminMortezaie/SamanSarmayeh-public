from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading

c = 0
f_list = ['''true==function()
{
        if( ((pmax)-(pmin))/(pl) >= 0.04 && (pf) == (pmin) && (pl) <=
(pmax)-((pmax)-(pmin))*0.05 && (pl) >= (pmax)-((pmax)-(pmin))*0.2)
        {
        return true;
    }
        else
        {
        return false;
    }
}()''', '''true==function()
{
        if( ((pmax)-(pmin))/(pl) >= 0.04 && (pf) >=
((pmin)+((pmax)-(pmin))*0.05) && (pf) <= ((pmin)+((pmax)-(pmin))*0.2)
&& (pl) >= (pmax)-((pmax)-(pmin))*0.05)
        {
        return true;
    }
        else
        {
        return false;
    }
}()''', '''true==function()
{
        if( ((pmax)-(pmin))/(pl) >= 0.04 && (pf) == (pmin) && (pl) <=
(pmax)-((pmax)-(pmin))*0.05 && (pl) >= (pmax)-((pmax)-(pmin))*0.2)
        {
        return true;
    }
        else
        {
        return false;
    }
}()''']

driver = webdriver.Chrome('chromedriver.exe')
url = 'http://www.tsetmc.com/Loader.aspx?ParTree=15131F#'
driver.get(url)


def scrape(filter_list=f_list, driver=driver, bot=None, chat_id=None, f_name=None):
    global f_list
    f_list = filter_list[:]
    # add filter
    e = driver.find_element_by_xpath('//*[@id="SettingsDesc"]/div[1]/a[7]')
    e.click()

    new_filter = driver.find_element_by_css_selector(
        '#FilterIndex > div.awesome.black')
    new_filter.click()

    selected_filter = driver.find_elements_by_xpath(
        '//*[@id="FilterIndex"]/div[1]')
    selected_filter[0].click()

    filter_area = driver.find_element_by_id('InputFilterCode')
    filter_area.send_keys(filter_list[0])

    save = driver.find_element_by_css_selector(
        '#FilterContent > div.awesome.blue')
    save.click()
    for i in range(len(filter_list)-1):
        add_next_filter = driver.find_element_by_css_selector(
            '#FilterIndex > div.awesome.black')
        add_next_filter.click()
    for i in range(1, len(filter_list)):
        filter_btn = driver.find_element_by_css_selector(
            '#FilterIndex > div:nth-child(%i)' % (i+2))
        filter_btn.click()
        filter_area = driver.find_element_by_id('InputFilterCode')
        filter_area.send_keys(filter_list[i])
        save = driver.find_element_by_css_selector(
            '#FilterContent > div.awesome.blue')
        save.click()

    return check_new(filter_list, bot=bot, chat_id=chat_id, f_name=f_name)


def check_new(filter_list, bot=None, chat_id=None, f_name=None):
    # fetch data
    # global shared_namad,shared_data,shared_intersect
    global c
    data = []
    namad = []
    for i in range(len(filter_list)):
        filter_btn = driver.find_element_by_css_selector(
            '#FilterIndex > div:nth-child(%i)' % (i+2))
        filter_btn.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.findAll('div', {'class': "{c}"})
        namad_list = []
        n = []
        for tag in a:
            d = {}
            d['namad'] = tag.find('a').text
            d['price'] = tag.find('div', {'class': "t0c t0c3 ch0"}).text
            n.append(d['namad'])
            namad_list.append(d)
        data.append(namad_list)
        namad.append(n)
    c += 1

    # intersection
    init = namad[0]
    for i in namad[1:]:
        s = list(set(init) & set(i))
        init = s
    # init is result
    print(init)
    s = ''
    for x in range(len(data)):
        s += 'اطلاعات {0}'.format(f_name[x])
        s += '\n'
        for d in data[x]:
            s += d['namad']
            s += '\t'
            s += d['price']
            s += '\n'
        s += '------------------------------------\n'
    if len(data) > 0:
        bot.sendMessage(chat_id, s)
    else:
        if c % 100 == 0:
            bot.sendMessage(chat_id, s)
            c = 0
    recheck(update=bot.getUpdates(), filter_list=filter_list,
            bot=bot, chat_id=chat_id, fname=f_name)


def recheck(update, filter_list, bot, chat_id, fname):
    if update != []:
        print(update[0]['message']['text'])
    else:
        # time.sleep(60)
        check_new(filter_list, bot, chat_id, fname)


def kill(driver=driver):
    driver.quit()
