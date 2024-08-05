from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PopularAppBots = Union["raw.types.bots.PopularAppBots"]


# noinspection PyRedeclaration
class PopularAppBots:  # type: ignore
    QUALNAME = "pyrogram.raw.base.bots.PopularAppBots"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
