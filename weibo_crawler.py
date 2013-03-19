#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'
from multiprocessing import Process

from xtimeline.actions.crawler import start as status_crawler
from xtimeline.actions.friendships import start as friendship_creator
from xtimeline.actions.publisher import start as status_poster


if __name__ == '__main__':
    crawler_process = Process(target=status_crawler)
    creator_process = Process(target=friendship_creator)
    #poster_process = Process(target=status_poster)
    crawler_process.start()
    creator_process.start()
    #poster_process.start()


