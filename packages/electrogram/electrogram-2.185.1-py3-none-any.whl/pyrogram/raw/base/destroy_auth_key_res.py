from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DestroyAuthKeyRes = Union["raw.types.DestroyAuthKeyFail", "raw.types.DestroyAuthKeyNone", "raw.types.DestroyAuthKeyOk"]


# noinspection PyRedeclaration
class DestroyAuthKeyRes:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DestroyAuthKeyRes"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
