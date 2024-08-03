from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedInfo = Union["raw.types.payments.SavedInfo"]


# noinspection PyRedeclaration
class SavedInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.SavedInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
