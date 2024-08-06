from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ServerDHInnerData = Union["raw.types.ServerDHInnerData"]


# noinspection PyRedeclaration
class ServerDHInnerData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ServerDHInnerData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
