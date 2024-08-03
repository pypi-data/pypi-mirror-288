from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TopPeerCategory = Union["raw.types.TopPeerCategoryBotsApp", "raw.types.TopPeerCategoryBotsInline", "raw.types.TopPeerCategoryBotsPM", "raw.types.TopPeerCategoryChannels", "raw.types.TopPeerCategoryCorrespondents", "raw.types.TopPeerCategoryForwardChats", "raw.types.TopPeerCategoryForwardUsers", "raw.types.TopPeerCategoryGroups", "raw.types.TopPeerCategoryPhoneCalls"]


# noinspection PyRedeclaration
class TopPeerCategory:  # type: ignore
    QUALNAME = "pyrogram.raw.base.TopPeerCategory"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
