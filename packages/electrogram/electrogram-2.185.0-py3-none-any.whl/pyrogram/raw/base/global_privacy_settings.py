from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GlobalPrivacySettings = Union["raw.types.GlobalPrivacySettings"]


# noinspection PyRedeclaration
class GlobalPrivacySettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.GlobalPrivacySettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
