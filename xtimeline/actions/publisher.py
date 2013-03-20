#!/usr/bin python
# -*- coding: utf-8 -*-
import time

__author__ = 'Tony.Shao'

from xtimeline.algorithms.top import scores
from xtimeline.helpers import when
from xtimeline.models.database import Statuses, WeiboAccounts
from xtimeline.libs.cache import SimpleCache
from xtimeline.helpers.weibo import statuses_repost

cache = SimpleCache()


def __get_top():
    statuses = Statuses.query.filter(Statuses.reposts_count > 100, Statuses.comments_count > 10, Statuses.counter > 5,
                                     Statuses.created_at >= when.past(hours=2)).all()
    for status in statuses:
        if cache.exists(status.wid):
            continue
        score = scores(comments_count=status.comments_count, reposts_count=status.reposts_count, counter=status.counter)
        status.score = score
    statuses = sorted(statuses, key=lambda status: status.score, reverse=True)
    if statuses:
        return statuses[0]


def publish():
    weibo_account = WeiboAccounts.query.filter(WeiboAccounts.status == 126).first()
    status = __get_top()
    if status is None:
        return
    statuses_repost(wid=status.wid, status="#实时热点推荐# 热门系数: " + str(round(status.score, 4) * 10),
                    access_token=weibo_account.access_token,
                    expires_in=weibo_account.expires_in)
    cache.store(status.wid, status.score)


def start():
    while True:
        publish()
        time.sleep(10 * 60)


if __name__ == '__main__':
    start()