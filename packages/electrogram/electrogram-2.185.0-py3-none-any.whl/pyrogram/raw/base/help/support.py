from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Support = Union["raw.types.help.Support"]


# noinspection PyRedeclaration
class Support:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.Support"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
