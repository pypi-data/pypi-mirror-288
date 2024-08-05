from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelParticipant = Union["raw.types.ChannelParticipant", "raw.types.ChannelParticipantAdmin", "raw.types.ChannelParticipantBanned", "raw.types.ChannelParticipantCreator", "raw.types.ChannelParticipantLeft", "raw.types.ChannelParticipantSelf"]


# noinspection PyRedeclaration
class ChannelParticipant:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChannelParticipant"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
