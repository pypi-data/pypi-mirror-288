from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SentCodeType = Union["raw.types.auth.SentCodeTypeApp", "raw.types.auth.SentCodeTypeCall", "raw.types.auth.SentCodeTypeEmailCode", "raw.types.auth.SentCodeTypeFirebaseSms", "raw.types.auth.SentCodeTypeFlashCall", "raw.types.auth.SentCodeTypeFragmentSms", "raw.types.auth.SentCodeTypeMissedCall", "raw.types.auth.SentCodeTypeSetUpEmailRequired", "raw.types.auth.SentCodeTypeSms", "raw.types.auth.SentCodeTypeSmsPhrase", "raw.types.auth.SentCodeTypeSmsWord"]


# noinspection PyRedeclaration
class SentCodeType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.SentCodeType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
