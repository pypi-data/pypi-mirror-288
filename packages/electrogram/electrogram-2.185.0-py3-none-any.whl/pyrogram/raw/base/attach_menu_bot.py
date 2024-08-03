from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AttachMenuBot = Union["raw.types.AttachMenuBot"]


# noinspection PyRedeclaration
class AttachMenuBot:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AttachMenuBot"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
