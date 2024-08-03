from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AccessPointRule = Union["raw.types.AccessPointRule"]


# noinspection PyRedeclaration
class AccessPointRule:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AccessPointRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
