from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelParticipant = Union["raw.types.channels.ChannelParticipant"]


# noinspection PyRedeclaration
class ChannelParticipant:  # type: ignore
    QUALNAME = "pyrogram.raw.base.channels.ChannelParticipant"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
