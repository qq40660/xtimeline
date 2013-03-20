#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__author__ = 'Tony.Shao'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from multiprocessing import Process

from xtimeline.actions.crawler import start as status_crawler
from xtimeline.actions.friendships import start as friendship_creator
from xtimeline.actions.publisher import start as status_creator


if __name__ == '__main__':
    crawler_process = Process(target=status_crawler)
    friendship_process = Process(target=friendship_creator)
    status_process = Process(target=status_creator)
    crawler_process.start()
    friendship_process.start()
    status_process.start()


