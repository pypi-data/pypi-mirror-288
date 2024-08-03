from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageExtendedMedia = Union["raw.types.MessageExtendedMedia", "raw.types.MessageExtendedMediaPreview"]


# noinspection PyRedeclaration
class MessageExtendedMedia:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageExtendedMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
