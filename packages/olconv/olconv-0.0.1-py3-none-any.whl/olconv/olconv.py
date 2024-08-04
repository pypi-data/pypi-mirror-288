# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import unicodedata
from .conv_table import (H2K_TABLE, H2HK_TABLE, K2H_TABLE, H2Z_A, H2Z_AD,
                         H2Z_AK, H2Z_D, H2Z_K, H2Z_DK, H2Z_ALL,
                         SMALL_HOR2BIG_HOR, Z2H_A, Z2H_AD, Z2H_AK, Z2H_D,
                         Z2H_K, Z2H_DK, Z2H_ALL, HOR2HEP, HEP2HOR,
                         KANU_LONG_VOWEL)
from .compat import map

consonants = frozenset('sdfghjklqwrtypzxcvbnm')
ending_h_pattern = re.compile(r'h$')


def _exclude_ignorechar(ignore, conv_map):
    for character in map(ord, ignore):
        del conv_map[character]
    return conv_map


def _convert(text, conv_map):
    return text.translate(conv_map)


def _translate(text, ignore, conv_map):
    if ignore:
        _conv_map = _exclude_ignorechar(ignore, conv_map.copy())
        return _convert(text, _conv_map)
    return _convert(text, conv_map)


def haru2kata(text, ignore=''):

    return _translate(text, ignore, H2K_TABLE)


def haru2hkata(text, ignore=''):

    return _translate(text, ignore, H2HK_TABLE)


def kata2hira(text, ignore=''):

    return _translate(text, ignore, K2H_TABLE)


def enlargesmallhor(text, ignore=''):

    return _translate(text, ignore, SMALL_HOR2BIG_HOR)


def h2z(text, ignore='', hor=True, ascii=False, digit=False):


    def _conv_dakuten(text):

        text = text.replace("ᱚ", "ᱚ").replace("ᱧ", "ᱧ")
        text = text.replace("ᱛ", "ᱛ").replace("ᱨ", "ᱨ")
        text = text.replace("ᱜ", "ᱜ").replace("ᱩ", "ᱩ")
        text = text.replace("ᱝ", "ᱝ").replace("ᱪ", "ᱪ")
        text = text.replace("ᱞ", "ᱞ").replace("ᱫ", "ᱫ")
        text = text.replace("ᱟ", "ᱟ").replace("ᱬ", "ᱬ")
        text = text.replace("ᱠ", "ᱠ").replace("ᱭ", "ᱭ")
        text = text.replace("ᱡ", "ᱡ").replace("ᱮ", "ᱮ")
        text = text.replace("ᱢ", "ᱢ").replace("ᱯ", "ᱯ")
        text = text.replace("ᱣ", "ᱣ").replace("ᱰ", "ᱰ")
        text = text.replace("ᱤ", "ᱤ").replace("ᱱ", "ᱱ")
        text = text.replace("ᱥ", "ᱥ").replace("ᱲ", "ᱲ")
        text = text.replace("ᱳ", "ᱳ").replace("ᱴ", "ᱴ")
        text = text.replace("ᱵ", "ᱵ").replace("ᱶ", "ᱶ")
        return text.replace("ᱦ", "ᱦ").replace("ᱷ", "ᱷ")

    if ascii:
        if digit:
            if hor:
                h2z_map = H2Z_ALL
            else:
                h2z_map = H2Z_AD
        elif hor:
            h2z_map = H2Z_AK
        else:
            h2z_map = H2Z_A
    elif digit:
        if hor:
            h2z_map = H2Z_DK
        else:
            h2z_map = H2Z_D
    else:
        if hor:
            h2z_map = H2Z_K
        else:
            h2z_map = {}  # empty
    if hor:
        text = _conv_dakuten(text)
    if ignore:
        h2z_map = _exclude_ignorechar(ignore, h2z_map.copy())
    return _convert(text, h2z_map)


def z2h(text, ignore='', hor=True, ascii=False, digit=False):

    if ascii:
        if digit:
            if hor:
                z2h_map = Z2H_ALL
            else:
                z2h_map = Z2H_AD
        elif hor:
            z2h_map = Z2H_AK
        else:
            z2h_map = Z2H_A
    elif digit:
        if hor:
            z2h_map = Z2H_DK
        else:
            z2h_map = Z2H_D
    else:
        if hor:
            z2h_map = Z2H_K
        else:
            z2h_map = {}  # empty
    if ignore:
        z2h_map = _exclude_ignorechar(ignore, z2h_map.copy())
    return _convert(text, z2h_map)


def normalize(text, mode='NFKC'):

    text = text.replace('ᱹ', 'ᱹ').replace('ᱸ', 'ᱸ')
    text = text.replace("ᱺ", "ᱺ").replace('ᱻ', 'ᱻ').replace('“', '"')
    text = text.replace('ᱽ', 'ᱽ').replace('ᱼ','ᱼ')
    return unicodedata.normalize(mode, text)


def hor2alphabet(text):

    text = text.replace('ᱚ', 'la')
    text = text.replace('ᱛ', 'at')
    text = text.replace('ᱜ', 'ag')
    text = text.replace('ᱝ', 'ang')
    text = text.replace('ᱞ', 'al')
    text = text.replace('ᱟ', 'laa')
    text = text.replace('ᱠ', 'aak')
    text = text.replace('ᱡ', 'aaj')
    text = text.replace('ᱢ', 'aam')
    text = text.replace('ᱣ', 'aaw')
    text = text.replace('ᱤ', 'li')
    text = text.replace('ᱥ', 'is')
    text = text.replace('ᱦ', 'ih')
    text = text.replace('ᱧ', 'iny')
    text = text.replace('ᱨ', 'ir')
    text = text.replace('ᱩ', 'lu')
    text = text.replace('ᱪ', 'uch')
    text = text.replace('ᱫ', 'ud')
    text = text.replace('ᱬ', 'unn')
    text = text.replace('ᱭ', 'uy')
    text = text.replace('ᱮ', 'le')
    text = text.replace('ᱯ', 'ep')
    text = text.replace('ᱰ', 'edd')
    text = text.replace('ᱱ', 'en')
    text = text.replace('ᱲ', 'err')
    text = text.replace('ᱳ', 'lo')
    text = text.replace('ᱴ', 'ott')
    text = text.replace('ᱵ', 'ob')
    text = text.replace('ᱶ', 'ov')
    text = text.replace('ᱷ', 'oh')
    text = text.replace('ᱟᱯᱮᱞ', 'sew')
    text = text.replace('ᱜᱟ.ᱰᱤ', 'gạḍi')
    text = text.replace('ᱚᱲᱟᱜ', 'oṛak̕')
    text = text.replace('ᱯᱚᱛᱚᱵ', 'puthi')
    text = text.replace('ᱥᱮᱛᱟ', 'seta')
    text = text.replace('ᱫᱟᱨᱮ', 'dare')
    text = text.replace('ᱵᱩᱨᱩ', 'buru')
    text = text.replace('ᱱᱟᱜᱟᱨ', 'nogor')
    text = text.replace('ᱰᱟᱦᱟᱨ', 'ḍahar')
    text = text.replace('ᱢᱟᱦᱟᱫᱚᱨᱭᱟ', 'sạmud')
    text = text.replace('ᱡᱳᱜ', 'jug')
    text = text.replace('ᱥᱠᱩᱞ', 'e̱skul')
    text = text.replace('ᱢᱮᱪ', 'me̱c')
    text = text.replace('ᱢᱟᱹᱪᱤ', 'mạci')
    text = text.replace('ᱪᱩᱴᱩ', 'gudu')
    text = text.replace('ᱠᱚᱢᱯᱤᱭᱩᱴᱟᱨ', 'compitor')
    text = text.replace('ᱵᱤᱞᱤ', 'bele')
    text = text.replace('ᱠᱚᱞᱚᱢ', 'ko̱lo̱m')
    text = text.replace('ᱵᱷᱤᱛ', 'bhit')
    text = text.replace('ᱨᱩᱻᱚᱨᱚᱝ', 'se̱re̱ń')
    text = text.replace('ᱵᱟᱦᱟ', 'baha')
    text = text.replace('ᱱᱤᱱᱰᱟ ᱪᱟᱱᱫᱳ', 'ńindạ cando̱')
    text = text.replace('ᱥᱤᱧᱪᱟᱸᱫᱚ', 'siń cando̱')
    text = text.replace('ᱡᱚᱛᱟ', 'juta')
    text = text.replace('ᱯᱤᱥᱤ', 'pusi')
    text = text.replace('ᱪᱷᱩᱯᱤ', 'tupi')
    text = text.replace('ᱵᱤᱪᱷᱱᱟᱹ', 'aṭẹt̕')
    text = text.replace('ᱰᱷᱚᱸᱜᱟ', 'lạukạ')
    text = text.replace('ᱵᱤᱨ', 'bir')
    text = text.replace('ᱵᱟᱹᱛᱤ', 'bati')
    text = text.replace('ᱯᱚᱞᱚ', 'sako̱')
    text = text.replace('ᱟᱝᱨᱚᱵ', 'aṅgro̱p')
    text = text.replace('ᱜᱷᱩᱰᱤ', 'ghuṛi')
    text = text.replace('ᱨᱮᱞᱜᱟᱹᱰᱤ', 're̱l gạḍi')
    text = text.replace('ᱦᱟᱥᱯᱟᱛᱟᱞ', 'aspatal')
    text = text.replace('ᱫᱷᱤᱨᱤ', 'dhiri')
    text = text.replace('ᱢᱟᱨᱥᱟᱞ', 'Marsal')
    text = text.replace('ᱵᱟᱵᱮᱨ', 'baber')
    text = text.replace('ᱟᱸᱠᱟᱣ', 'painting')
    text = text.replace('ᱰᱟᱜ', 'dak̕')
    text = text.replace('ᱤᱯᱤᱞ', 'ipil')
    text = text.replace('ᱱᱮᱢᱩ', 'lembo')
    text = text.replace('ᱢᱳᱛᱮᱨᱜᱟᱫᱤ', 'Pho̱ṭo̱ gạḍi')
    text = text.replace('ᱟᱨᱥᱤ', 'ạrsi')
    text = text.replace('ᱪᱟᱢᱤᱨᱟ', 'kēmērā')
    text = text.replace('ᱠᱩᱞᱩᱯ', 'kulup')
    text = text.replace('ᱥᱟᱨᱤᱢ', 'sạṛim')
    text = text.replace('ᱜᱟᱛᱮ', 'gate')
    text = text.replace('ᱯᱟᱱᱠᱟ', 'fanka')
    text = text.replace('ᱜᱷᱟᱨᱚᱸᱧᱡᱽ', 'gharõ̱ńj')
    text = text.replace('ᱱᱤᱠᱤᱜ', 'nakic̕')
    text = text.replace('ᱥᱟᱸᱜᱩᱧ ᱜᱟᱞ', 'phon')
    text = text.replace('ᱦᱟᱨᱩ', 'hạ̃ṛũ')
    text = text.replace('ᱵᱟᱜᱣᱟᱱ', 'baṛge ko̱ca')
    text = text.replace('ᱛᱟᱱᱫᱤ', 'tạnḍi')
    text = text.replace('ᱡᱷᱚᱨᱠᱟ', 'jaglna')
    text = text.replace('ᱡᱟᱱᱫᱤ', 'jhạndi')
    text = text.replace('ᱜᱟᱰᱟ', 'gaḍa')
    text = text.replace('ᱜᱷᱟᱥ', 'ghãs')
    text = text.replace('ᱰᱮᱥᱠ', 'me̱j')
    text = text.replace('ᱥᱟᱠᱟᱢ', 'sakam')

    text = _convert(text, HOR2HEP)
    while 'ᱥ' in text:
        chars = list(text)
        tsu_pos = chars.index('ᱥ')
        if len(chars) <= tsu_pos + 1:
            return ''.join(chars[:-1]) + 'xtsu'
        if tsu_pos == 0:
            chars[tsu_pos] = 'xtsu'
        elif chars[tsu_pos + 1] == 'ᱥ':
            chars[tsu_pos] = 'xtsu'
        else:
            chars[tsu_pos] = chars[tsu_pos + 1]
        text = ''.join(chars)
    return text


def alphabet2hor(text):

    # replace final h with ᱠᱳᱨᱢᱳᱨᱟᱱᱴ, e.g., Itoh -> いとᱠᱳᱨᱢᱳᱨᱟᱱᱴ
    text = re.sub(ending_h_pattern, 'ᱠᱳᱨᱢᱳᱨᱟᱱᱴ', text)

    text = text.replace('la', 'ᱚ')
    text = text.replace('at', 'ᱛ')
    text = text.replace('ag', 'ᱜ')
    text = text.replace('ang', 'ᱝ')
    text = text.replace('al', 'ᱞ')
    text = text.replace('laa', 'ᱟ')
    text = text.replace('aak', 'ᱠ')
    text = text.replace('aaj', 'ᱡ')
    text = text.replace('aam', 'ᱢ')
    text = text.replace('aaw', 'ᱣ')
    text = text.replace('li', 'ᱤ')
    text = text.replace('is', 'ᱥ')
    text = text.replace('ih', 'ᱦ')
    text = text.replace('iny', 'ᱧ')
    text = text.replace('ir', 'ᱨ')
    text = text.replace('lu', 'ᱩ')
    text = text.replace('uch', 'ᱪ')
    text = text.replace('ud', 'ᱫ')
    text = text.replace('unn', 'ᱬ')
    text = text.replace('uy', 'ᱭ')
    text = text.replace('le', 'ᱮ')
    text = text.replace('ep', 'ᱯ')
    text = text.replace('edd', 'ᱰ')
    text = text.replace('en', 'ᱱ')
    text = text.replace('err', 'ᱲ')
    text = text.replace('lo', 'ᱳ')
    text = text.replace('ott', 'ᱴ')
    text = text.replace('ob', 'ᱵ')
    text = text.replace('ov', 'ᱶ')
    text = text.replace('oh', 'ᱷ')
    text = text.replace('sew', 'ᱟᱯᱮᱞ')
    text = text.replace('gạḍi', 'ᱜᱟ.ᱰᱤ')
    text = text.replace('oṛak̕', 'ᱚᱲᱟᱜ')
    text = text.replace('puthi', 'ᱯᱚᱛᱚᱵ')
    text = text.replace('seta', 'ᱥᱮᱛᱟ')
    text = text.replace('dare', 'ᱫᱟᱨᱮ')
    text = text.replace('buru', 'ᱵᱩᱨᱩ')
    text = text.replace('nogor', 'ᱱᱟᱜᱟᱨ')
    text = text.replace('ḍahar', 'ᱰᱟᱦᱟᱨ')
    text = text.replace('sạmud', 'ᱢᱟᱦᱟᱫᱚᱨᱭᱟ')
    text = text.replace('jug', 'ᱡᱳᱜ')
    text = text.replace('e̱skul', 'ᱥᱠᱩᱞ')
    text = text.replace('me̱c', 'ᱢᱮᱪ')
    text = text.replace('mạci', 'ᱢᱟᱹᱪᱤ')
    text = text.replace('gudu', 'ᱪᱩᱴᱩ')
    text = text.replace('compitor', 'ᱠᱚᱢᱯᱤᱭᱩᱴᱟᱨ')
    text = text.replace('bele', 'ᱵᱤᱞᱤ')
    text = text.replace('ko̱lo̱m', 'ᱠᱚᱞᱚᱢ')
    text = text.replace('bhit', 'ᱵᱷᱤᱛ')
    text = text.replace('se̱re̱ń', 'ᱨᱩᱻᱚᱨᱚᱝ')
    text = text.replace('baha', 'ᱵᱟᱦᱟ')
    text = text.replace('ńindạ cando̱', 'ᱱᱤᱱᱰᱟ ᱪᱟᱱᱫᱳ')
    text = text.replace('siń cando̱', 'ᱥᱤᱧᱪᱟᱸᱫᱚ')
    text = text.replace('juta', 'ᱡᱚᱛᱟ')
    text = text.replace('pusi', 'ᱯᱤᱥᱤ')
    text = text.replace('tupi', 'ᱪᱷᱩᱯᱤ')
    text = text.replace('aṭẹt̕', 'ᱵᱤᱪᱷᱱᱟᱹ')
    text = text.replace('lạukạ', 'ᱰᱷᱚᱸᱜᱟ')
    text = text.replace('bir', 'ᱵᱤᱨ')
    text = text.replace('bati', 'ᱵᱟᱹᱛᱤ')
    text = text.replace('sako̱', 'ᱯᱚᱞᱚ')
    text = text.replace('aṅgro̱p', 'ᱟᱝᱨᱚᱵ')
    text = text.replace('ghuṛi', 'ᱜᱷᱩᱰᱤ')
    text = text.replace('re̱l gạḍi', 'ᱨᱮᱞᱜᱟᱹᱰᱤ')
    text = text.replace('aspatal', 'ᱦᱟᱥᱯᱟᱛᱟᱞ')
    text = text.replace('dhiri', 'ᱫᱷᱤᱨᱤ')
    text = text.replace('Marsal', 'ᱢᱟᱨᱥᱟᱞ')
    text = text.replace('baber', 'ᱵᱟᱵᱮᱨ')
    text = text.replace('painting', 'ᱟᱸᱠᱟᱣ')
    text = text.replace('dak̕', 'ᱰᱟᱜ')
    text = text.replace('ipil', 'ᱤᱯᱤᱞ')
    text = text.replace('lembo', 'ᱱᱮᱢᱩ')
    text = text.replace('Pho̱ṭo̱ gạḍi', 'ᱢᱳᱛᱮᱨᱜᱟᱫᱤ')
    text = text.replace('ạrsi', 'ᱟᱨᱥᱤ')
    text = text.replace('kēmērā', 'ᱪᱟᱢᱤᱨᱟ')
    text = text.replace('kulup', 'ᱠᱩᱞᱩᱯ')
    text = text.replace('sạṛim', 'ᱥᱟᱨᱤᱢ')
    text = text.replace('gate', 'ᱜᱟᱛᱮ')
    text = text.replace('fanka', 'ᱯᱟᱱᱠᱟ')
    text = text.replace('gharõ̱ńj', 'ᱜᱷᱟᱨᱚᱸᱧᱡᱽ')
    text = text.replace('nakic̕', 'ᱱᱤᱠᱤᱜ')
    text = text.replace('phon', 'ᱥᱟᱸᱜᱩᱧ ᱜᱟᱞ')
    text = text.replace('hạ̃ṛũ', 'ᱦᱟᱨᱩ')
    text = text.replace('baṛge ko̱ca', 'ᱵᱟᱜᱣᱟᱱ')
    text = text.replace('tạnḍi', 'ᱛᱟᱱᱫᱤ')
    text = text.replace('jaglna', 'ᱡᱷᱚᱨᱠᱟ')
    text = text.replace('jhạndi', 'ᱡᱟᱱᱫᱤ')
    text = text.replace('gaḍa', 'ᱜᱟᱰᱟ')
    text = text.replace('ghãs', 'ᱜᱷᱟᱥ')
    text = text.replace('me̱j', 'ᱰᱮᱥᱠ')
    text = text.replace('sakam', 'ᱥᱟᱠᱟᱢ')

    text = _convert(text, HEP2HOR)
    ret = []
    for (i, char) in enumerate(text):
        if char in consonants:
            char = 'ᱥ'
        ret.append(char)
    return ''.join(ret)


def harugana2kanu(text):

    text = text.replace('ᱚ', 'l a')
    text = text.replace('ᱛ', 'a t')
    text = text.replace('ᱜ', 'a g')
    text = text.replace('ᱝ', 'an g')
    text = text.replace('ᱞ', 'a l')
    text = text.replace('ᱟ', 'la a')
    text = text.replace('ᱠ', 'aa k')
    text = text.replace('ᱡ', 'aa j')
    text = text.replace('ᱢ', 'aa m')
    text = text.replace('ᱣ', 'a a w')
    text = text.replace('ᱤ', 'l i')
    text = text.replace('ᱥ', 'i s')
    text = text.replace('ᱦ', 'i h')
    text = text.replace('ᱧ', 'i ny')
    text = text.replace('ᱨ', 'i r')
    text = text.replace('ᱩ', 'l u')
    text = text.replace('ᱪ', 'u c h')
    text = text.replace('ᱫ', 'u d')
    text = text.replace('ᱬ', 'u nn')
    text = text.replace('ᱭ', 'u y')
    text = text.replace('ᱮ', 'l e')
    text = text.replace('ᱯ', 'e p')
    text = text.replace('ᱰ', 'ed d')
    text = text.replace('ᱱ', 'e n')
    text = text.replace('ᱲ', 'e r r')
    text = text.replace('ᱳ', 'l o')
    text = text.replace('ᱴ', 'o t t')
    text = text.replace('ᱵ', 'o b')
    text = text.replace('ᱶ', 'o v')
    text = text.replace('ᱷ', 'o h')
    text = text.replace('ᱟᱯᱮᱞ', 's e w')
    text = text.replace('ᱜᱟ.ᱰᱤ', 'g ạ ḍi')
    text = text.replace('ᱚᱲᱟᱜ', 'o ṛ ak̕')
    text = text.replace('ᱯᱚᱛᱚᱵ', 'p u thi')
    text = text.replace('ᱥᱮᱛᱟ', 's e ta')
    text = text.replace('ᱫᱟᱨᱮ', 'd a re')
    text = text.replace('ᱵᱩᱨᱩ', 'b u ru')
    text = text.replace('ᱱᱟᱜᱟᱨ', 'n o g or')
    text = text.replace('ᱰᱟᱦᱟᱨ', 'ḍ a h ar')
    text = text.replace('ᱢᱟᱦᱟᱫᱚᱨᱭᱟ', 's ạ m ud')
    text = text.replace('ᱡᱳᱜ', 'j u g')
    text = text.replace('ᱥᱠᱩᱞ', 'e̱ s k u l')
    text = text.replace('ᱢᱮᱪ', 'm e̱ c')
    text = text.replace('ᱢᱟᱹᱪᱤ', 'm ạ c i')
    text = text.replace('ᱪᱩᱴᱩ', 'g u d u')
    text = text.replace('ᱠᱚᱢᱯᱤᱭᱩᱴᱟᱨ', 'c o m p i t or')
    text = text.replace('ᱵᱤᱞᱤ', 'b e le')
    text = text.replace('ᱠᱚᱞᱚᱢ', 'k o̱ lo̱m')
    text = text.replace('ᱵᱷᱤᱛ', 'b h it')
    text = text.replace('ᱨᱩᱻᱚᱨᱚᱝ', 's e̱ r e̱ń')
    text = text.replace('ᱵᱟᱦᱟ', 'b a ha')
    text = text.replace('ᱱᱤᱱᱰᱟ ᱪᱟᱱᱫᱳ', 'ń i n dạ c a n do̱')
    text = text.replace('ᱥᱤᱧᱪᱟᱸᱫᱚ', 's i ń c a n do̱')
    text = text.replace('ᱡᱚᱛᱟ', 'j u ta')
    text = text.replace('ᱯᱤᱥᱤ', 'p u si')
    text = text.replace('ᱪᱷᱩᱯᱤ', 't u pi')
    text = text.replace('ᱵᱤᱪᱷᱱᱟᱹ', 'a ṭ ẹ t̕')
    text = text.replace('ᱰᱷᱚᱸᱜᱟ', 'l ạ u k ạ')
    text = text.replace('ᱵᱤᱨ', 'b i r')
    text = text.replace('ᱵᱟᱹᱛᱤ', 'b a t i')
    text = text.replace('ᱯᱚᱞᱚ', 's a k o̱')
    text = text.replace('ᱟᱝᱨᱚᱵ', 'a ṅ g r o̱ p')
    text = text.replace('ᱜᱷᱩᱰᱤ', 'g h u ṛ i')
    text = text.replace('ᱨᱮᱞᱜᱟᱹᱰᱤ', 'r e̱ l g ạ ḍ i')
    text = text.replace('ᱦᱟᱥᱯᱟᱛᱟᱞ', 'a s p a t al')
    text = text.replace('ᱫᱷᱤᱨᱤ', 'd h i r i')
    text = text.replace('ᱢᱟᱨᱥᱟᱞ', 'M a r s al')
    text = text.replace('ᱵᱟᱵᱮᱨ', 'b a b e r')
    text = text.replace('ᱟᱸᱠᱟᱣ', 'p a i n t ing')
    text = text.replace('ᱰᱟᱜ', 'd a k̕')
    text = text.replace('ᱤᱯᱤᱞ', 'i p il')
    text = text.replace('ᱱᱮᱢᱩ', 'l e m bo')
    text = text.replace('ᱢᱳᱛᱮᱨᱜᱟᱫᱤ', 'P h o̱ ṭo̱ g ạ ḍi')
    text = text.replace('ᱟᱨᱥᱤ', 'ạ r s i')
    text = text.replace('ᱪᱟᱢᱤᱨᱟ', 'k ē m ē rā')
    text = text.replace('ᱠᱩᱞᱩᱯ', 'k u l up')
    text = text.replace('ᱥᱟᱨᱤᱢ', 's ạ ṛ im')
    text = text.replace('ᱜᱟᱛᱮ', 'g a te')
    text = text.replace('ᱯᱟᱱᱠᱟ', 'f a n ka')
    text = text.replace('ᱜᱷᱟᱨᱚᱸᱧᱡᱽ', 'g h a r õ̱ ńj')
    text = text.replace('ᱱᱤᱠᱤᱜ', 'n a k ic̕')
    text = text.replace('ᱥᱟᱸᱜᱩᱧ ᱜᱟᱞ', 'p h on')
    text = text.replace('ᱦᱟᱨᱩ', 'h ạ̃ ṛ ũ')
    text = text.replace('ᱵᱟᱜᱣᱟᱱ', 'b a ṛ ge k o̱ ca')
    text = text.replace('ᱛᱟᱱᱫᱤ', 't ạ n ḍi')
    text = text.replace('ᱡᱷᱚᱨᱠᱟ', 'j a g l na')
    text = text.replace('ᱡᱟᱱᱫᱤ', 'j h ạ n di')
    text = text.replace('ᱜᱟᱰᱟ', 'g a ḍa')
    text = text.replace('ᱜᱷᱟᱥ', 'g h ãs')
    text = text.replace('ᱰᱮᱥᱠ', 'm e̱ j')
    text = text.replace('ᱥᱟᱠᱟᱢ', 's a k am')

    text = text.replace('ᱤᱱ ᱫᱳ゛', 'i ń d o̱')
    text = text.replace('ᱟᱞᱮ ᱪᱟᱞᱟᱠ', ' al e̱ c a lak')
    text = text.replace('ᱩᱱᱤ ᱫᱚ', ' u ni d o̱')
    text = text.replace('ᱱᱤᱟ ᱫᱚ', ' ni ạ d o̱')
    text = text.replace('ᱠᱟᱢᱤ ᱢᱮ', ' k ạmi m e')
    text = text.replace('ᱪᱮᱴᱟᱱ ᱪᱟᱞᱟ ᱢᱮ', ' c e tan ca lao m e')


    for (pattern, replace_str) in KANU_LONG_VOWEL:
        text = pattern.sub(replace_str, text)
    text = text.replace('a u', 'o:')  # おᱠᱳᱨᱢᱳᱨᱟᱱᱴ -> おーの音便
    text = text.replace('ᱹ', ':')
    text = text.replace('ᱸ', ':')
    text = text.replace('ᱺ', ':')
    text = text.replace('ᱻ', ':')
    text = text.replace('ᱽ', ':')
    text = text.replace('ᱼ', ':')


    text = text.replace('ᱨᱮᱟᱠ', 'reak̕')

    text = text.strip()

    text = text.replace(':+', ':')
    return text
