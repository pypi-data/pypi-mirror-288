from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RecentMeUrls = Union["raw.types.help.RecentMeUrls"]


# noinspection PyRedeclaration
class RecentMeUrls:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.RecentMeUrls"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
