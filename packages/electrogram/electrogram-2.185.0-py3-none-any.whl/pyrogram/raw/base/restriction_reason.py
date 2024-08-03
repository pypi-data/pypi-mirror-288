from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RestrictionReason = Union["raw.types.RestrictionReason"]


# noinspection PyRedeclaration
class RestrictionReason:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RestrictionReason"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
