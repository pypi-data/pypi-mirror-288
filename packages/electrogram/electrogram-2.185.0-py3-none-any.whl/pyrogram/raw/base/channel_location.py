from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelLocation = Union["raw.types.ChannelLocation", "raw.types.ChannelLocationEmpty"]


# noinspection PyRedeclaration
class ChannelLocation:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChannelLocation"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
