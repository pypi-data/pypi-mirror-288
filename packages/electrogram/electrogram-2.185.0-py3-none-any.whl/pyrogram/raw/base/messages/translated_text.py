from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TranslatedText = Union["raw.types.messages.TranslateResult"]


# noinspection PyRedeclaration
class TranslatedText:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.TranslatedText"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
