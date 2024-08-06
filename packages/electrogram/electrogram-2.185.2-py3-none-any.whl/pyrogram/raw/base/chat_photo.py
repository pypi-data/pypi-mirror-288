from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatPhoto = Union["raw.types.ChatPhoto", "raw.types.ChatPhotoEmpty"]


# noinspection PyRedeclaration
class ChatPhoto:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatPhoto"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
