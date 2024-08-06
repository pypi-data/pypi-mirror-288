from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputFolderPeer = Union["raw.types.InputFolderPeer"]


# noinspection PyRedeclaration
class InputFolderPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputFolderPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
