from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

HighScores = Union["raw.types.messages.HighScores"]


# noinspection PyRedeclaration
class HighScores:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.HighScores"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
