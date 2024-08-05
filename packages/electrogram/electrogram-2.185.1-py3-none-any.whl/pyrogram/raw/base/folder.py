from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Folder = Union["raw.types.Folder"]


# noinspection PyRedeclaration
class Folder:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Folder"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
