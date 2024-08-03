from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EligibilityToJoin = Union["raw.types.smsjobs.EligibleToJoin"]


# noinspection PyRedeclaration
class EligibilityToJoin:  # type: ignore
    QUALNAME = "pyrogram.raw.base.smsjobs.EligibilityToJoin"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
