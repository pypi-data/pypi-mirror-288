from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RecentMeUrl = Union["raw.types.RecentMeUrlChat", "raw.types.RecentMeUrlChatInvite", "raw.types.RecentMeUrlStickerSet", "raw.types.RecentMeUrlUnknown", "raw.types.RecentMeUrlUser"]


# noinspection PyRedeclaration
class RecentMeUrl:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RecentMeUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
