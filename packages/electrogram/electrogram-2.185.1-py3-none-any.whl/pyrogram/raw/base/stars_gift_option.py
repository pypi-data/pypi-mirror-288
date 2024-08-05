from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsGiftOption = Union["raw.types.StarsGiftOption"]


# noinspection PyRedeclaration
class StarsGiftOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StarsGiftOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
