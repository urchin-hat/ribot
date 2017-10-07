# coding: utf-8

import random
import datetime
import slackbot_settings
import pya3rt
import urllib.request
from bs4 import BeautifulSoup
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

@respond_to('はろー')
def mention_func(message):
    log_output(message)
    message.reply('ハローワールド')

@respond_to('新書')
@respond_to('書籍')
def new_book(message):
    log_output(message)
    try:
        html = urllib.request.urlopen("https://www.oreilly.co.jp/index.shtml")
        soup = BeautifulSoup(html, "html.parser")
        new_book = soup.find("div", { "class" : "post" })
        text  = new_book.h3.string + '\n\n'
        text += '。\n'.join((new_book.find('img')['title'].split('。')))
        text += new_book.find('img')['src']
    except Exception as e:
        text = '情報が取得できません＞＜'

    message.reply(text)

@listen_to('お疲れ様です')
def listen_func(message):
    log_output(message)
    message.send('誰かがお疲れ様ですと言ったね')
    message.reply('君だね？')

@respond_to(r'^おにぎり$')
@listen_to('今日のおにぎり')
def onigiri(message):
    log_output(message)
    # おにぎりランキング https://matome.naver.jp/odai/2134359745609300101
    onigiri_list = ['ツナマヨネーズ','しゃけ','梅干し','明太子','焼きたらこ','昆布','いくら','えびマヨネーズ','おかか','筋子',
                    'とり五目','高菜','天むす','明太子マヨネーズ','生たらこ','辛子明太子','唐揚げ','焼きサケハラミ','焼肉','マグロ']
    message.reply('今日のおすすめは *' + str(random.choice(onigiri_list)) + '* だよ！')

@default_reply()
def default_func(message):
    log_output(message)
    client = pya3rt.TalkClient(slackbot_settings.A3RT_API_KEY)
    try:
        message.reply(str((client.talk(str(message._body['text'])))["results"][0]["reply"]))
    except Exception as e:
        message.reply("ちょっと何言ってるかわかりません")

def log_output(message):
    # import inspect; print(inspect.getmembers(message))
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S\t' + message._body['user'] + '\t' + message._body['text']))
