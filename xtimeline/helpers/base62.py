#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Tony.Shao'

__all__ = ('encode', 'decode',)

LETTERS, SIZE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 62
DICT = dict((char, index) for index, char in enumerate(LETTERS))

def div_util(num, dividend):
    while True:
        num, index = divmod(num, dividend)
        yield index
        if num == 0:
            return

decode = lambda str_: sum(DICT[char] * (SIZE ** (index)) for index, char in enumerate(str_[::-1]))

encode = lambda num: ''.join(LETTERS[index] for index in div_util(num, SIZE))[::-1]

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
def get_url(mid):
    if not isinstance(mid, str):
        mid = str(mid)
    mid = list(mid)
    mid.reverse()
    mid_chunks = list(chunks(mid, 7))
    url = []
    for chunk in mid_chunks:
        chunk.reverse()
        _char = encode(int(''.join(chunk)))
        _char = _char.rjust(4, '0')
        url.append(_char)
    url.reverse()
    return ''.join(url).lstrip('0')

#zavn10pSv
if __name__ == '__main__':
    print get_url('3525038710099479')

