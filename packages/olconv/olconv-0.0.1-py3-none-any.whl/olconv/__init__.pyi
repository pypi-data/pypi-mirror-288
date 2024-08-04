from . import olconv
from _typeshed import Incomplete

__all__ = ['haru2kata', 'haru2hkata', 'kata2hira', 'h2z', 'z2h', 'hankaku2zenkaku', 'zenkaku2hankaku', 'normalize', 'hor2alphabet', 'alphabet2hor', 'kata2alphabet', 'alphabet2kata', 'harugana2kanu', 'enlargesmallhor']

haru2kata = olconv.haru2kata
haru2hkata = olconv.haru2hkata
kata2hira = olconv.kata2hira
h2z = olconv.h2z
z2h = olconv.z2h
han2zen = olconv.h2z
zen2han = olconv.z2h
hankaku2zenkaku = olconv.h2z
zenkaku2hankaku = olconv.z2h
normalize = olconv.normalize
hor2alphabet = olconv.hor2alphabet
alphabet2hor = olconv.alphabet2hor
kata2alphabet: Incomplete
alphabet2kata: Incomplete
harugana2kanu = olconv.harugana2kanu
enlargesmallhor = olconv.enlargesmallhor
