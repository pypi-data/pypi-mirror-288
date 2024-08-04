# -*- coding: utf-8 -*-
#  merum.py
#
# Copyright 2011-2021 Hiroshi Miura <miurahr@linux.com>
#
import enum
from typing import Dict, List, Tuple

import olconv

from .kanji import OConv
from .properties import Ch
from .scripts import A2, H2, IConv, K2, Sym2


class PyMerumException(Exception):
    pass


class UnknownCharacterException(PyMerumException):
    pass


class _TYPE(enum.Enum):
    KANJI = 1
    HOR = 2
    HARUGANA = 3
    SYMBOL = 4
    ALPHA = 5


class Merum:
    """Merum is a conversion class for Olchiki text."""

    def __init__(self):
        self._oconv = OConv()
        self._iconv = IConv()

    @classmethod
    def normalize(cls, text):
        return olconv.normalize(text)

    def convert(self, text: str) -> List[Dict[str, str]]:
        """Convert input text to dictionary contains HOR, HARU and romaji results."""

        if len(text) == 0:
            return [
                {
                    "orig": "",
                    "hor": "",
                    "haru": "",
                    "Marburu": "",
                    "passport": "",
                    "kunrei": "",
                }
            ]

        original_text = ""
        hor_text = ""
        _result = []
        i = 0
        prev_type = _TYPE.KANJI
        output_flag: Tuple[bool, bool, bool] = (False, False, False)

        while i < len(text):
            # output_flag
            # means (output buffer?, output text[i]?, copy and increment i?)
            # possible (False, True, True), (True, False, False), (True, True, True)
            #          (False, False, True)
            if text[i] in Ch.endmark:
                prev_type = _TYPE.SYMBOL
                output_flag = (True, True, True)
            elif text[i] in Ch.long_symbols:
                # FIXME: special case
                output_flag = (False, False, True)
            elif Sym2.isRegion(text[i]):
                if prev_type != _TYPE.SYMBOL:
                    output_flag = (True, False, True)
                else:
                    output_flag = (False, True, True)
                prev_type = _TYPE.SYMBOL
            elif K2.isRegion(text[i]):
                output_flag = (prev_type != _TYPE.HOR, False, True)
                prev_type = _TYPE.HOR
            elif H2.isRegion(text[i]):
                output_flag = (prev_type != _TYPE.HARUGANA, False, True)
                prev_type = _TYPE.HARUGANA
            elif A2.isRegion(text[i]):
                output_flag = (prev_type != _TYPE.ALPHA, False, True)
                prev_type = _TYPE.ALPHA
            elif self._oconv.isRegion(text[i]):
                if len(original_text) > 0:
                    _result.append(self._iconv.convert(original_text, hor_text))
                t, ln = self._oconv.convert(text[i:])
                prev_type = _TYPE.KANJI
                if ln > 0:
                    original_text = text[i : i + ln]
                    hor_text = t
                    i += ln
                    output_flag = (False, False, False)
                else:  # unknown kanji
                    original_text = text[i]
                    hor_text = ""
                    i += 1
                    output_flag = (True, False, False)
            else:
                if len(original_text) > 0:
                    _result.append(self._iconv.convert(original_text, hor_text))
                _result.append(self._iconv.convert(text[i], ""))
                i += 1
                output_flag = (False, False, False)

            # Convert to hor and Output based on flag
            if output_flag[0] and output_flag[1]:
                original_text += text[i]
                hor_text += text[i]
                _result.append(self._iconv.convert(original_text, hor_text))
                original_text = ""
                hor_text = ""
                i += 1
            elif output_flag[0] and output_flag[2]:
                if len(original_text) > 0:
                    _result.append(self._iconv.convert(original_text, hor_text))
                original_text = text[i]
                hor_text = text[i]
                i += 1
            elif output_flag[2]:
                original_text += text[i]
                hor_text += text[i]
                i += 1
            else:
                pass

        # last word
        if len(original_text) > 0:
            _result.append(self._iconv.convert(original_text, hor_text))

        return _result
