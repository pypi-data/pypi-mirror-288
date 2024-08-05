from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelAdminLogEventsFilter = Union["raw.types.ChannelAdminLogEventsFilter"]


# noinspection PyRedeclaration
class ChannelAdminLogEventsFilter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChannelAdminLogEventsFilter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
