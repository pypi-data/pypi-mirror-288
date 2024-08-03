from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelDifference = Union["raw.types.updates.ChannelDifference", "raw.types.updates.ChannelDifferenceEmpty", "raw.types.updates.ChannelDifferenceTooLong"]


# noinspection PyRedeclaration
class ChannelDifference:  # type: ignore
    QUALNAME = "pyrogram.raw.base.updates.ChannelDifference"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
