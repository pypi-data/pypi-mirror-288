from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

HighScore = Union["raw.types.HighScore"]


# noinspection PyRedeclaration
class HighScore:  # type: ignore
    QUALNAME = "pyrogram.raw.base.HighScore"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
