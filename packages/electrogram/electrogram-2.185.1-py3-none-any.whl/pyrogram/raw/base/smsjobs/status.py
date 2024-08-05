from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Status = Union["raw.types.smsjobs.Status"]


# noinspection PyRedeclaration
class Status:  # type: ignore
    QUALNAME = "pyrogram.raw.base.smsjobs.Status"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
