from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedGroupCallInvite = Union["raw.types.phone.ExportedGroupCallInvite"]


# noinspection PyRedeclaration
class ExportedGroupCallInvite:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.ExportedGroupCallInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
