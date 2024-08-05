from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedMessageLink = Union["raw.types.ExportedMessageLink"]


# noinspection PyRedeclaration
class ExportedMessageLink:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ExportedMessageLink"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
