# coding: utf-8

import datetime
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

@respond_to('はろー')
def mention_func(message):
    log_output(message)
    message.reply('ハローワールド')

@listen_to('お疲れ様です')
def listen_func(message):
    log_output(message)
    message.send('誰かがお疲れ様ですと言ったね')
    message.reply('君だね？')

def log_output(message):
    # import inspect; print(inspect.getmembers(message))
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S\t' + message._body['user'] + '\t' + message._body['text']))
