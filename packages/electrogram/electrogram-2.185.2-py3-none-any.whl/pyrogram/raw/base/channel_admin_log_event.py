from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelAdminLogEvent = Union["raw.types.ChannelAdminLogEvent"]


# noinspection PyRedeclaration
class ChannelAdminLogEvent:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChannelAdminLogEvent"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
