from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReceivedNotifyMessage = Union["raw.types.ReceivedNotifyMessage"]


# noinspection PyRedeclaration
class ReceivedNotifyMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReceivedNotifyMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
