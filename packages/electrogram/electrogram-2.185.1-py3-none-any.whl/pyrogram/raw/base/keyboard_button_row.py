from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

KeyboardButtonRow = Union["raw.types.KeyboardButtonRow"]


# noinspection PyRedeclaration
class KeyboardButtonRow:  # type: ignore
    QUALNAME = "pyrogram.raw.base.KeyboardButtonRow"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
