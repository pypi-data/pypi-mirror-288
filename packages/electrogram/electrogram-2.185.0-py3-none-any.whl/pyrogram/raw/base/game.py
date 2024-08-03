from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Game = Union["raw.types.Game"]


# noinspection PyRedeclaration
class Game:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Game"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
