from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AdminLogResults = Union["raw.types.channels.AdminLogResults"]


# noinspection PyRedeclaration
class AdminLogResults:  # type: ignore
    QUALNAME = "pyrogram.raw.base.channels.AdminLogResults"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
