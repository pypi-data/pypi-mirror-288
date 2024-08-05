from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PrivacyRules = Union["raw.types.account.PrivacyRules"]


# noinspection PyRedeclaration
class PrivacyRules:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.PrivacyRules"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
