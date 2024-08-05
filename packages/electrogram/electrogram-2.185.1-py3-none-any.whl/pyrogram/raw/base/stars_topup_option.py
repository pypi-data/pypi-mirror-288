from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsTopupOption = Union["raw.types.StarsTopupOption"]


# noinspection PyRedeclaration
class StarsTopupOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StarsTopupOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
