from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ClientDHInnerData = Union["raw.types.ClientDHInnerData"]


# noinspection PyRedeclaration
class ClientDHInnerData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ClientDHInnerData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
