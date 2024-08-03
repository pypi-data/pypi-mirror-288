from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebAuthorization = Union["raw.types.WebAuthorization"]


# noinspection PyRedeclaration
class WebAuthorization:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WebAuthorization"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
