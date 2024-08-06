from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChannelParticipantsFilter = Union["raw.types.ChannelParticipantsAdmins", "raw.types.ChannelParticipantsBanned", "raw.types.ChannelParticipantsBots", "raw.types.ChannelParticipantsContacts", "raw.types.ChannelParticipantsKicked", "raw.types.ChannelParticipantsMentions", "raw.types.ChannelParticipantsRecent", "raw.types.ChannelParticipantsSearch"]


# noinspection PyRedeclaration
class ChannelParticipantsFilter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChannelParticipantsFilter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
