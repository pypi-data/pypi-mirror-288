from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedChatlistInvite = Union["raw.types.chatlists.ExportedChatlistInvite"]


# noinspection PyRedeclaration
class ExportedChatlistInvite:  # type: ignore
    QUALNAME = "pyrogram.raw.base.chatlists.ExportedChatlistInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
