#!/usr/bin/env python -u
# coding: utf-8

import sys
import random
import datetime
import json
import urllib.request
import urllib.parse
import feedparser
import pya3rt
import slackbot_settings
from bs4 import BeautifulSoup
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

# manual version
__version__ = "1.0"
__date__    = "2017/10/19"

# manual text
manual = '使い方を説明するよー [Ver' + __version__ + ' ' + __date__ + ']\n'\
         '>>> _- メンションが必要なもの(1on1なら不必要)_\n'\
         '\t_完全一致じゃないと反応しないもの_\n'\
         '\t\t_1) `はろー`と呟くと ハローワールドと返してくれるよー_\n'\
         '\t\t_2) `{都市名}の天気`と呟くと天気情報を教えてくれるよー_\n'\
         '\t\t_3) `BTCのレート`と呟くとBTCの売値買値を教えてくれるよー_\n'\
         '\t\t_4) `おにぎり`はおにぎり_\n'\
         '\t_引数がいるもの_\n'\
         '\t\t_1) `wiki {調べたいこと}`でwikipediaのページを教えてくれるよー\n\n'
         '_- メンションじゃなくても拾ってくれるもの(チャンネル限定)_\n'\
         '\t_完全一致じゃないと反応しないもの_\n'\
         '\t\t_1) `お疲れ様です`と呟くと返してくれるよー_\n'\
         '\t\t_2) `今日のおにぎり`はおにぎり_\n'\
         '\t_引数がいるもの_\n'\
         '\t\t_1) `選出 ○人`と呟くとランダムで選出してくれるよー_\n'\
         '\t\t_2) `アンケート お題 項目1 項目2...`と呟くとアンケートを作成するよー_\n'\
         '\t\t_3) `トピック 設定するトピック`と呟くとトピックを設定するよー_\n\n'\
         '_- どっちでも反応してくれるもの_\n'\
         '\t_完全一致じゃないと反応しないもの_\n'\
         '\t\t_1) `新書` or `書籍` or `新刊`と呟くとオライリーの新書情報を教えてくれるよー_\n'
         '\t\t_2) ニュースと呟くとスラドの最新5件のニュースを教えてくれるよー_\n\n'\
         '_それ以外はA3RTのTalk APIで塩対応してくれるよー_'

@respond_to(r'^はろー$')
def mention_func(message):
    log_output(message)
    message.reply('ハローワールド')

@listen_to(r'^お疲れ様です$')
def listen_func(message):
    log_output(message)
    message.send('おつかれさまー')

@respond_to(r'^help$|^ヘルプ$')
def help_func(message):
    global manual
    log_output(message)
    message.reply(manual)

@respond_to(r'^新書$|^書籍$|^新刊$')
@listen_to(r'^新書$|^書籍$|^新刊$')
def new_book_func(message):
    log_output(message)
    try:
        html = urllib.request.urlopen("https://www.oreilly.co.jp/index.shtml")
        soup = BeautifulSoup(html, "html.parser")
        new_book = soup.find("div", { "class" : "post" })
        text  = 'オライリーの新刊は *' + new_book.h3.string + '* だよー\n'
        text += new_book.find('a')['href']
    except Exception as e:
        text = '情報が取得できません＞＜'

    message.send(text)

@respond_to(r'^ニュース$')
@listen_to(r'^ニュース$')
def get_news_func(message):
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
    message.send(text)

@respond_to(r'^.*の天気$')
def weather_news_func(message):
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

@respond_to(r'^BTCのレート$')
def btc_rate_func(message):
    log_output(message)
    api_url = 'https://bitflyer.jp/api/echo/price'
    text = ''
    try:
        jsonfile = json.loads(urllib.request.urlopen(api_url).read())
        text = "> " + str(datetime.datetime.now().strftime('%Y年%m月%d日 %H時%M分')) + 'の\n'
        for key, value in jsonfile.items():
            if key == 'ask':
                text += '> ビットコイン購入（円）は' + '{:,}'.format(value) + '円\n'
            elif key == 'bid':
                text += '> ビットコイン売却（円）は' + '{:,}'.format(value) + '円\n'
        text += 'ですー'
    except Exception as e:
        text = '情報が取得できません＞＜'

    message.send(text)

@listen_to(r'^選出 (.*)人')
def random_choice_func(message, params):
    log_output(message)
    text = ''
    menbaers_list = []
    if params.isdigit():
        url = 'https://slack.com/api/channels.list?token=' + slackbot_settings.API_TOKEN + '&pretty=1'
        html = urllib.request.urlopen(url)
        jsonfile = json.loads(html.read().decode('utf-8'))
        channel_id = message._body['channel']
        try:
            for i in range(len(jsonfile['channels'])):
                if channel_id in jsonfile['channels'][i]['id']:
                    menbaers_list = jsonfile['channels'][i]['members']
                    for user_id in slackbot_settings.del_list:
                        try:
                            menbaers_list.remove(user_id)
                        except Exception as e:
                            pass
                    break
            for user_id in random.sample(menbaers_list, int(params)):
                text += "<@" + user_id + "> "
            text += "\n選ばれました！\nよろしくお願いしますm(_ _)m"
        except Exception as e:
            text = 'なんかエラーになった＞＜'
        message.send(text)
    else:
        message.reply('数値じゃない何かがはいったぬ')

# ref http://blog.bitmeister.jp/?p=3981
@listen_to(r'^アンケート (.*)')
def questionnaire_func(message, params):
    log_output(message)
    args = params.split(' ')
    if len(args) < 3:
        message.reply('`アンケート タイトル [質問 質問 ...]`と入力してー')
        return

    title = args.pop(0)
    options = []
    EMOJIS = ('one','two','three','four','five',)
    for i, o in enumerate(args):
        options.append('* :{}: {}'.format(EMOJIS[i], o))

    send_user = message.channel._client.users[message.body['user']][u'name']
    post = {
        'pretext': '<!channel> {}さんからアンケートがあります。'.format(send_user),
        'title': title,
        'author_name': send_user,
        'text': '\n'.join(options),
        'color': 'good'
    }

    ret = message._client.webapi.chat.post_message(
        message._body['channel'],
        '',
        username=message._client.login_data['self']['name'],
        as_user=True,
        attachments=[post]
    )
    ts = ret.body['ts']

    for i, _ in enumerate(options):
        message._client.webapi.reactions.add(
            name=EMOJIS[i],
            channel=message._body['channel'],
            timestamp=ts
        )

@respond_to(r'^wiki (.*)$')
def wikipedia_func(message, params):
    url = 'https://ja.wikipedia.org/wiki/' + urllib.parse.quote_plus(str(params).replace(' ', ''), encoding="utf-8")

    try:
        urllib.request.urlopen(url)
        text = 'Wikipediaの' + str(params).replace(' ', '') + 'の項目だよー\n' + url
    except urllib.request.HTTPError as e:
        if e.code != 200:
            text = '項目が見つかんないよ＞＜'

    message.reply(text)

@respond_to(r'^コマンド (.*)$')
def teach_cmd_func(message, params):
    url = 'http://www.k4.dion.ne.jp/~mms/unix/linux_com/' + str(params) + '.html'
     try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        text = '>>>*' + param[0] + '*\n'
        text += '\t機能\n'
        text += '\t\t' + soup.find("p", { "class" : "kinou" }).get_text() + '\n'
        text += '\t書式\n'
        text += '\t\t' + soup.find("p", { "class" : "opt" }).get_text()
    except urllib.request.HTTPError as e:
        if e.code != 200:
            text = '項目が見つかんないよー。または取ってきてるサイトにのってないです＞＜'

    message.reply(text)

@listen_to(r'^トピック (.*)$')
def set_topic_func(message, params):
    log_output(message)
    message.send('トピックを設定するよー')
    url = 'https://slack.com/api/channels.setTopic?token=' + slackbot_settings.API_TOKEN + '&channel=' + message._body['channel'] + '&topic=' + urllib.parse.quote_plus(params, encoding='utf-8')
    urllib.request.urlopen(url)

@respond_to(r'^おにぎり$')
@listen_to(r'^今日のおにぎり$')
def onigiri_func(message):
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
    # import inspect; print(inspect.getmembers(message)) # debug
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S\t' + message._body['user'] + '\t' + message._body['text']))
    sys.stdout.flush()
