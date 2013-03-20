#!/usr/bin python
# -*- coding: utf-8 -*-
import time
import traceback
import sys

__author__ = 'Tony.Shao'

from xtimeline.algorithms.top import scores
from xtimeline.helpers import when
from xtimeline.models.database import Statuses, WeiboAccounts
from xtimeline.libs.cache import SimpleCache
from xtimeline.helpers.weibo import statuses_repost

cache = SimpleCache(limit=100, set_name='xtimeline')


def __get_top():
    statuses = Statuses.query.filter(Statuses.reposts_count > 100, Statuses.comments_count > 10, Statuses.counter > 5,
                                     Statuses.created_at >= when.past(hours=2)).all()
    scored_statuses = []
    for status in statuses:
        if cache.exists(status.wid):
            continue
        score = scores(comments_count=status.comments_count, reposts_count=status.reposts_count, counter=status.counter)
        status.score = score
        scored_statuses.append(status)
    statuses = sorted(statuses, key=lambda scored_statuses: status.score, reverse=True)
    if statuses:
        return statuses[0]


def publish():
    weibo_account = WeiboAccounts.query.filter(WeiboAccounts.status == 126).first()
    status = __get_top()
    if status is None:
        return
    statuses_repost(wid=status.wid, status="#实时热点推荐# 热度: " + str(round(status.score, 4) * 10) + "°",
                    access_token=weibo_account.access_token,
                    expires_in=weibo_account.expires_in)
    cache.store(status.wid, status.score)
    print status.wid


def start():
    while True:
        try:
            publish()
        except Exception:
            print traceback.format_exc()
        finally:
            sys.stdout.flush()
            time.sleep(10 * 60)


if __name__ == '__main__':
    start()