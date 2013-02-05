#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'
from xtimeline.actions.crawler import start as status_crawler
from xtimeline.actions.friendships import start as friendship_creator

from multiprocessing import Process

if __name__ == '__main__':
    crawler_process = Process(target=status_crawler)
    creator_process = Process(target=friendship_creator)
    crawler_process.start()
    creator_process.start()

