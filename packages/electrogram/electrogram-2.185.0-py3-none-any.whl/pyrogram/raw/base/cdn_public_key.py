from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CdnPublicKey = Union["raw.types.CdnPublicKey"]


# noinspection PyRedeclaration
class CdnPublicKey:  # type: ignore
    QUALNAME = "pyrogram.raw.base.CdnPublicKey"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
