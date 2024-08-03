from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AttachMenuBotIconColor = Union["raw.types.AttachMenuBotIconColor"]


# noinspection PyRedeclaration
class AttachMenuBotIconColor:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AttachMenuBotIconColor"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
