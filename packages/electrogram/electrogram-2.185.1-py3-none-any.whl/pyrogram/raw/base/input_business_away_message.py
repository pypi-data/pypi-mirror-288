from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBusinessAwayMessage = Union["raw.types.InputBusinessAwayMessage"]


# noinspection PyRedeclaration
class InputBusinessAwayMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBusinessAwayMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
