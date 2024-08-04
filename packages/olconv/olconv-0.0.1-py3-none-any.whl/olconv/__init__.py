# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import olconv


VERSION = (0, 0, 1)
__version__ = '0.0.1'
__all__ = [
    'haru2kata', 'haru2hkata', 'kata2hira', 'h2z', 'z2h', 'hankaku2zenkaku',
    'zenkaku2hankaku', 'normalize', 'hor2alphabet', 'alphabet2hor',
    'kata2alphabet', 'alphabet2kata', 'harugana2kanu', 'enlargesmallhor'
]

haru2kata = olconv.haru2kata
haru2hkata = olconv.haru2hkata
kata2hira = olconv.kata2hira
h2z = olconv.h2z
z2h = olconv.z2h
han2zen = olconv.h2z  # an alias of h2z
zen2han = olconv.z2h  # an alias of z2h
hankaku2zenkaku = olconv.h2z  # an alias of h2z
zenkaku2hankaku = olconv.z2h  # an alias of z2h
normalize = olconv.normalize
hor2alphabet = olconv.hor2alphabet
alphabet2hor = olconv.alphabet2hor
kata2alphabet = lambda text: olconv.hor2alphabet(olconv.kata2hira(text))
alphabet2kata = lambda text: olconv.haru2kata(olconv.alphabet2hor(text))
harugana2kanu = olconv.harugana2kanu
enlargesmallhor = olconv.enlargesmallhor
