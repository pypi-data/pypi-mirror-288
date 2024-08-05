from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputGame = Union["raw.types.InputGameID", "raw.types.InputGameShortName"]


# noinspection PyRedeclaration
class InputGame:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputGame"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
