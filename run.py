#!/usr/bin/env python -u
# coding: utf-8

import sys, datetime
from slackbot.bot import Bot

def main():
    try:
        bot = Bot()
        bot.run()
    except Exception as e:
        sys.exit(1)

if __name__ == '__main__':
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S\tstart'))
    main()
