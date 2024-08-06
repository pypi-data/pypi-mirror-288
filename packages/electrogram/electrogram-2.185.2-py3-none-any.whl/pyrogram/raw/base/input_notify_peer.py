from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputNotifyPeer = Union["raw.types.InputNotifyBroadcasts", "raw.types.InputNotifyChats", "raw.types.InputNotifyForumTopic", "raw.types.InputNotifyPeer", "raw.types.InputNotifyUsers"]


# noinspection PyRedeclaration
class InputNotifyPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputNotifyPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
