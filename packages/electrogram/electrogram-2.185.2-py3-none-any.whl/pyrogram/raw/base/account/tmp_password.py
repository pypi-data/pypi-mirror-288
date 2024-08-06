from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TmpPassword = Union["raw.types.account.TmpPassword"]


# noinspection PyRedeclaration
class TmpPassword:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.TmpPassword"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
