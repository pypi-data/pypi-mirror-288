from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotPreviewMedia = Union["raw.types.BotPreviewMedia"]


# noinspection PyRedeclaration
class BotPreviewMedia:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotPreviewMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
