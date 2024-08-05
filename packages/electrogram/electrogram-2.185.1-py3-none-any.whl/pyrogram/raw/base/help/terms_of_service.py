from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TermsOfService = Union["raw.types.help.TermsOfService"]


# noinspection PyRedeclaration
class TermsOfService:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.TermsOfService"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
