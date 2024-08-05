from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DefaultHistoryTTL = Union["raw.types.DefaultHistoryTTL"]


# noinspection PyRedeclaration
class DefaultHistoryTTL:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DefaultHistoryTTL"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
