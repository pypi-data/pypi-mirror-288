from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PreviewInfo = Union["raw.types.bots.PreviewInfo"]


# noinspection PyRedeclaration
class PreviewInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.bots.PreviewInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
