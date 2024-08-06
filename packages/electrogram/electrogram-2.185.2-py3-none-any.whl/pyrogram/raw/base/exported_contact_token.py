from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedContactToken = Union["raw.types.ExportedContactToken"]


# noinspection PyRedeclaration
class ExportedContactToken:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ExportedContactToken"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
