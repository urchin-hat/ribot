# coding: utf-8

import random
import datetime
import json
import slackbot_settings
import pya3rt
import urllib.request
import feedparser
from bs4 import BeautifulSoup
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

@respond_to('はろー')
def mention_func(message):
    log_output(message)
    message.reply('ハローワールド')

@respond_to(r'^新書$')
@respond_to(r'^書籍$')
def new_book(message):
    log_output(message)
    try:
        html = urllib.request.urlopen("https://www.oreilly.co.jp/index.shtml")
        soup = BeautifulSoup(html, "html.parser")
        new_book = soup.find("div", { "class" : "post" })
        text  = 'オライリーの新刊は *' + new_book.h3.string + '* だよー\n'
        text += new_book.find('a')['href']
    except Exception as e:
        text = '情報が取得できません＞＜'

    message.reply(text)

@respond_to(r'^ニュース$')
def get_news(message):
    log_output(message)
    RSS_URL = "https://srad.jp/sradjp.rss"

    try:
        rss = feedparser.parse(RSS_URL)
        text = 'スラド(https://srad.jp/)の新着のニュースだよー\n>>> '
        for i in range(0,5):
            text += str(i + 1) + ') ' + rss['entries'][i]['title'] + ' - (' + rss['entries'][i]['link'] + ')\n'
        text = text.rstrip('\n')
    except Exception as e:
        text = '情報が取得できません＞＜'
    message.reply(text)

@respond_to(r'^.*の天気$')
def weather_news(message):
    log_output(message)
    city = message._body['text'].split('の')[0]
    url = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
    try:
        html = urllib.request.urlopen("http://weather.livedoor.com/forecast/rss/primary_area.xml")
        soup = BeautifulSoup(html, "html.parser")
        if soup.find("city", { "title" : city }) != None:
            text = city + 'の天気だよー\n'
            city_id = soup.find("city", { "title" : city })['id']
            html = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=' + city_id)
            jsonfile = json.loads(html.read().decode('utf-8'))
            text += '>>> ' + jsonfile['description']['text']
        else:
            text = '{0}の地域IDが見つからないようです。\n以下のURLを参考にしてください。\n{1}'.format(city, url)
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
