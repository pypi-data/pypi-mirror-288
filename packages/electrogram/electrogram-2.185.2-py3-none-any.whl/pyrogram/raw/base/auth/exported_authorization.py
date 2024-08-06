from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedAuthorization = Union["raw.types.auth.ExportedAuthorization"]


# noinspection PyRedeclaration
class ExportedAuthorization:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.ExportedAuthorization"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
