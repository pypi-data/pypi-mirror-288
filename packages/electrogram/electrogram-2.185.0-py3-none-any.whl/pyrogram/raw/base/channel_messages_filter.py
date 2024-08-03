from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelMessagesFilter = Union["raw.types.ChannelMessagesFilter", "raw.types.ChannelMessagesFilterEmpty"]


# noinspection PyRedeclaration
class ChannelMessagesFilter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChannelMessagesFilter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
