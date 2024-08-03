from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CodeType = Union["raw.types.auth.CodeTypeCall", "raw.types.auth.CodeTypeFlashCall", "raw.types.auth.CodeTypeFragmentSms", "raw.types.auth.CodeTypeMissedCall", "raw.types.auth.CodeTypeSms"]


# noinspection PyRedeclaration
class CodeType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.CodeType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
