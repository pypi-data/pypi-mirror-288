from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ResolvedPeer = Union["raw.types.contacts.ResolvedPeer"]


# noinspection PyRedeclaration
class ResolvedPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.ResolvedPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
