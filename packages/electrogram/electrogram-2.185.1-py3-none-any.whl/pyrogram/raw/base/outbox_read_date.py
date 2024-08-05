from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

OutboxReadDate = Union["raw.types.OutboxReadDate"]


# noinspection PyRedeclaration
class OutboxReadDate:  # type: ignore
    QUALNAME = "pyrogram.raw.base.OutboxReadDate"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
