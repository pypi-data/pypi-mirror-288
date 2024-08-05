from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedInvites = Union["raw.types.chatlists.ExportedInvites"]


# noinspection PyRedeclaration
class ExportedInvites:  # type: ignore
    QUALNAME = "pyrogram.raw.base.chatlists.ExportedInvites"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
