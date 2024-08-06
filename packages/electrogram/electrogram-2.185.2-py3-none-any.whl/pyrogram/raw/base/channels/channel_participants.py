from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelParticipants = Union["raw.types.channels.ChannelParticipants", "raw.types.channels.ChannelParticipantsNotModified"]


# noinspection PyRedeclaration
class ChannelParticipants:  # type: ignore
    QUALNAME = "pyrogram.raw.base.channels.ChannelParticipants"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
