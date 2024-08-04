# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from .compat import map, zip

HARUGANA = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽᱼᱷᱛᱷᱜᱷᱠᱷᱡᱷᱪᱷᱫᱷᱯᱷᱰᱷ ᱲᱷᱴᱷᱵᱷ'
                'ᱩᱥᱩᱠ ᱪᱮᱫᱟᱜ ᱳᱱᱚᱞᱟᱹᱭ ᱟᱰᱤ ᱢᱚᱡ ᱪᱚᱨᱚᱠ ᱵᱟᱝ  ᱦᱳᱭ ᱯᱷᱩᱞ ᱪᱟᱞᱟᱜ ᱵᱷᱟᱹᱜᱤ ᱵᱟᱨ ᱵᱩᱨᱩ ᱛᱤ ᱟᱨ ᱢᱤᱫ ᱠᱚᱨᱟᱣ ᱪᱮᱫ ᱷᱚᱸ ᱵᱟᱝ ᱪᱮᱛᱟᱱ ᱵᱚᱢ ᱞᱟᱦᱟ ᱟᱜ ᱴᱟᱜ ᱡᱩᱫᱤ ᱯᱟᱯᱟ ᱥᱤᱧ ᱪᱟᱸᱫᱚ ᱥᱩᱱᱩᱢ ᱯᱟᱭ'
                'ᱢᱤᱱᱟᱥ ᱫᱟᱜ ᱛᱮᱦᱮᱧ ᱛᱮ ᱛᱟᱦᱮᱱ ᱰᱩᱞᱟᱨ ᱫᱟᱨᱮ ᱠᱟ.ᱴᱤᱡᱼᱜᱤᱫᱽᱨᱟ. ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸ'
                'ᱩᱛᱱᱟᱹᱣ ᱦᱮᱸ ᱽ ᱚᱱᱚᱞᱤᱭᱟᱹ ᱟᱞᱮ ᱮ ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣ ᱹ ᱸ ᱺ ᱻ ᱽ ᱼ')
HALF_ASCII = list('!"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  '[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ')
HALF_DIGIT = list('0123456789')
HALF_HOR_ROR = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽᱼᱷᱛᱷᱜᱷᱠᱷᱡᱷᱪᱷᱫᱷᱯᱷᱰᱷᱲᱷᱴᱷᱵᱷ'
                       'ᱩᱛᱱᱟᱹᱣ ᱦᱮᱸ ᱽ ᱚᱱᱚᱞᱤᱭᱟᱹ ᱟᱞᱮ ᱮ ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣ ᱹ ᱸ ᱺ ᱻ ᱽ ᱼ')
HALF_HOR = ['ᱚ', 'ᱛ', 'ᱜ', 'ᱝ', 'ᱞ', 'ᱟ', 'ᱠ', 'ᱡ', 'ᱢ', 'ᱣ', 'ᱤ', 'ᱥ', 'ᱦ', 'ᱧ', 'ᱨ', 'ᱩ', 'ᱪ', 'ᱫ', 'ᱬ', 'ᱭ', 'ᱮ', 'ᱯ', 'ᱰ', 'ᱱ', 'ᱲ', 'ᱳ', 'ᱴ', 'ᱵ', 'ᱶ', 'ᱷ', 'ᱹ', 'ᱸ', 'ᱺ', 'ᱻ', 'ᱽ', 'ᱼ', 'ᱷ', 'ᱛ', 'ᱷ', 'ᱜ', 'ᱷ', 'ᱠ', 'ᱷ', 'ᱡ', 'ᱷ', 'ᱪ', 'ᱷ', 'ᱫ', 'ᱷ', 'ᱯ', 'ᱷ', 'ᱰ', 'ᱷ']
FULL_ASCII = list('！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠'
                  'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
                  '［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔ'
                  'ｕｖｗｘｙｚ｛｜｝～　')
FULL_DIGIT = list('０１２３４５６７８９')
FULL_HOR = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽᱼᱷᱛᱷᱜᱷᱠᱷᱡᱷᱪᱷᱫᱷᱯᱷᱰᱷ ᱲᱷᱴᱷᱵᱷ'
                 'ᱢᱤᱱᱟᱥ ᱫᱟᱜ ᱛᱮᱦᱮᱧ ᱛᱮ ᱛᱟᱦᱮᱱ ᱰᱩᱞᱟᱨ ᱫᱟᱨᱮ ᱠᱟ.ᱴᱤᱡᱼᱜᱤᱫᱽᱨᱟ. ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸ'
                 'ᱢᱤᱱᱟᱥ ᱫᱟᱜ ᱛᱮᱦᱮᱧ ᱛᱮ ᱛᱟᱦᱮᱱ ᱰᱩᱞᱟᱨ ᱫᱟᱨᱮ ᱠᱟ.ᱴᱤᱡᱼᱜᱤᱫᱽᱨᱟ. ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸ'
                 'ᱹ ᱸ ᱺ ᱻ ᱽ ᱼ')
FULL_HOR_ROR = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽᱼᱷᱛᱷᱜᱷᱠᱷᱡᱷᱪᱷᱫᱷᱯᱷᱰᱷ ᱲᱷᱴᱷᱵᱷ'
                       'ᱢᱤᱱᱟᱥ ᱫᱟᱜ ᱛᱮᱦᱮᱧ ᱛᱮ ᱛᱟᱦᱮᱱ ᱰᱩᱞᱟᱨ ᱫᱟᱨᱮ ᱠᱟ.ᱴᱤᱡᱼᱜᱤᱫᱽᱨᱟ. ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸ'
                       'ᱩᱛᱱᱟᱹᱣ ᱦᱮᱸ ᱽ ᱚᱱᱚᱞᱤᱭᱟᱹ ᱟᱞᱮ ᱮ ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣ ᱹ ᱸ ᱺ ᱻ ᱽ ᱼ')
MARBURU = list('aiueoaiueon')
MARBURU_HOR = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽ')
SMALL_HOR = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽᱼᱷᱛᱷᱜᱷᱠᱷᱡᱷᱪᱷᱫᱷᱯᱷᱰᱷ ᱲᱷᱴᱷᱵᱷ')
SMALL_HOR_NORMALIZED = list('ᱚᱛᱜᱝᱞᱟᱠᱡᱢᱣᱤᱥᱦᱧᱨᱩᱪᱫᱬᱭᱮᱯᱰᱱᱲᱳᱴᱵᱶᱷᱹᱸᱺᱻᱽᱼᱷᱛᱷᱜᱷᱠᱷᱡᱷᱪᱷᱫᱷᱯᱷᱰᱷᱲᱷᱴᱷᱵᱷ')


def _to_ord_list(chars):
    return list(map(ord, chars))


HARUGANA_ORD = _to_ord_list(HARUGANA)
FULL_HOR_ORD = _to_ord_list(FULL_HOR)
HALF_ASCII_ORD = _to_ord_list(HALF_ASCII)
FULL_ASCII_ORD = _to_ord_list(FULL_ASCII)
HALF_DIGIT_ORD = _to_ord_list(HALF_DIGIT)
FULL_DIGIT_ORD = _to_ord_list(FULL_DIGIT)
HALF_HOR_ROR_ORD = _to_ord_list(HALF_HOR_ROR)
FULL_HOR_ROR_ORD = _to_ord_list(FULL_HOR_ROR)
SMALL_HOR_ORD = _to_ord_list(SMALL_HOR)


def _to_dict(_from, _to):
    return dict(zip(_from, _to))


H2K_TABLE = _to_dict(HARUGANA_ORD, FULL_HOR)
H2HK_TABLE = _to_dict(HARUGANA_ORD, HALF_HOR)
K2H_TABLE = _to_dict(FULL_HOR_ORD, HARUGANA)

H2Z_A = _to_dict(HALF_ASCII_ORD, FULL_ASCII)
H2Z_AD = _to_dict(HALF_ASCII_ORD+HALF_DIGIT_ORD, FULL_ASCII+FULL_DIGIT)
H2Z_AK = _to_dict(HALF_ASCII_ORD+HALF_HOR_ROR_ORD,
                  FULL_ASCII+FULL_HOR_ROR)
H2Z_D = _to_dict(HALF_DIGIT_ORD, FULL_DIGIT)
H2Z_K = _to_dict(HALF_HOR_ROR_ORD, FULL_HOR_ROR)
H2Z_DK = _to_dict(HALF_DIGIT_ORD+HALF_HOR_ROR_ORD,
                  FULL_DIGIT+FULL_HOR_ROR)
H2Z_ALL = _to_dict(HALF_ASCII_ORD+HALF_DIGIT_ORD+HALF_HOR_ROR_ORD,
                   FULL_ASCII+FULL_DIGIT+FULL_HOR_ROR)

Z2H_A = _to_dict(FULL_ASCII_ORD, HALF_ASCII)
Z2H_AD = _to_dict(FULL_ASCII_ORD+FULL_DIGIT_ORD, HALF_ASCII+HALF_DIGIT)
Z2H_AK = _to_dict(FULL_ASCII_ORD+FULL_HOR_ORD, HALF_ASCII+HALF_HOR)
Z2H_D = _to_dict(FULL_DIGIT_ORD, HALF_DIGIT)
Z2H_K = _to_dict(FULL_HOR_ORD, HALF_HOR)
Z2H_DK = _to_dict(FULL_DIGIT_ORD+FULL_HOR_ORD, HALF_DIGIT+HALF_HOR)
Z2H_ALL = _to_dict(FULL_ASCII_ORD+FULL_DIGIT_ORD+FULL_HOR_ORD,
                   HALF_ASCII+HALF_DIGIT+HALF_HOR)
HOR2HEP = _to_dict(_to_ord_list(MARBURU_HOR), MARBURU)
HEP2HOR = _to_dict(_to_ord_list(MARBURU), MARBURU_HOR)

KANU_LONG_VOWEL = tuple(
    (
        (re.compile('( a){2,}'), ' a:'),
        (re.compile('( i){2,}'), ' i:'),
        (re.compile('( u){2,}'), ' u:'),
        (re.compile('( e){2,}'), ' e:'),
        (re.compile('( o){2,}'), ' o:')
    )
)

SMALL_HOR2BIG_HOR = _to_dict(SMALL_HOR_ORD, SMALL_HOR_NORMALIZED)

del _to_ord_list
del _to_dict
del HARUGANA_ORD
del HARUGANA
del HALF_HOR
del FULL_HOR_ORD
del FULL_HOR
del HALF_ASCII_ORD
del HALF_ASCII
del FULL_ASCII_ORD
del FULL_ASCII
del HALF_DIGIT_ORD
del HALF_DIGIT
del FULL_DIGIT_ORD
del FULL_DIGIT
del HALF_HOR_ROR_ORD
del HALF_HOR_ROR
del FULL_HOR_ROR_ORD
del FULL_HOR_ROR
del MARBURU
del MARBURU_HOR
del SMALL_HOR
del SMALL_HOR_ORD
del SMALL_HOR_NORMALIZED
