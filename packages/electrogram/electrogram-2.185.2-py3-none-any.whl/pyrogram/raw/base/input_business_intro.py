from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBusinessIntro = Union["raw.types.InputBusinessIntro"]


# noinspection PyRedeclaration
class InputBusinessIntro:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBusinessIntro"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
