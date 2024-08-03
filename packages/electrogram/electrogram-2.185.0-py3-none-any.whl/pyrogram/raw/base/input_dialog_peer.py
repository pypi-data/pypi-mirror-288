from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputDialogPeer = Union["raw.types.InputDialogPeer", "raw.types.InputDialogPeerFolder"]


# noinspection PyRedeclaration
class InputDialogPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputDialogPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
