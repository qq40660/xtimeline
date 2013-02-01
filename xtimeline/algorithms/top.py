#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import log

__author__ = 'Tony.Shao'


def hot(reposts_count, comments_count, created_at, weight=1):
    return log(reposts_count + comments_count + weight)

def _calculate():
    pass