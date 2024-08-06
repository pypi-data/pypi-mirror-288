from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SendAsPeer = Union["raw.types.SendAsPeer"]


# noinspection PyRedeclaration
class SendAsPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SendAsPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
