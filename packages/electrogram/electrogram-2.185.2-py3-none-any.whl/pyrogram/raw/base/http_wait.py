from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

HttpWait = Union["raw.types.HttpWait"]


# noinspection PyRedeclaration
class HttpWait:  # type: ignore
    QUALNAME = "pyrogram.raw.base.HttpWait"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
