from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FolderPeer = Union["raw.types.FolderPeer"]


# noinspection PyRedeclaration
class FolderPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.FolderPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
