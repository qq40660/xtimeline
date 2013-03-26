#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'
from math import log


def scores(reposts_count, comments_count, counter=1):
    if comments_count > reposts_count:
        comments_count = reposts_count + (comments_count - reposts_count) * 0.1
    if comments_count < reposts_count * 0.1:
        reposts_count = comments_count + (reposts_count - comments_count) * 0.1
    return log(reposts_count * 0.2 + comments_count * 5 + counter * 400)
