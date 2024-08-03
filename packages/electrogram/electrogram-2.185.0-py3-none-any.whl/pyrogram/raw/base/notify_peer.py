from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

NotifyPeer = Union["raw.types.NotifyBroadcasts", "raw.types.NotifyChats", "raw.types.NotifyForumTopic", "raw.types.NotifyPeer", "raw.types.NotifyUsers"]


# noinspection PyRedeclaration
class NotifyPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.NotifyPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
