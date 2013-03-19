#!/usr/bin python
# -*- coding: utf-8 -*-
import sys

__author__ = 'Tony.Shao'

from xtimeline.models.database import WeiboAccounts
from xtimeline.helpers.weibo import get_home_timeline
from xtimeline.helpers.storage import store_timeline
###############################################################
import time
import random
import traceback


def crawler():
    """
    crawler start....GO GO GO GO
    """
    weibo_accounts = WeiboAccounts.query.filter(WeiboAccounts.status == 1,
                                                WeiboAccounts.expires_in > int(time.time())).all()
    for account in weibo_accounts:
        try:
            statuses = get_home_timeline(access_token=account.access_token, expires_in=account.expires_in)
            counts = store_timeline(statuses)
            print counts
            sys.stdout.flush()
        except Exception:
            print traceback.format_exc()
        finally:
            time.sleep(1 * random.randint(1, 10))


def start():
    while True:
        crawler()
        time.sleep(60)


if __name__ == '__main__':
    start()