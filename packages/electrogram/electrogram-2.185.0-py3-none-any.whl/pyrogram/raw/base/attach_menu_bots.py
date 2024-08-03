from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AttachMenuBots = Union["raw.types.AttachMenuBots", "raw.types.AttachMenuBotsNotModified"]


# noinspection PyRedeclaration
class AttachMenuBots:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AttachMenuBots"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
