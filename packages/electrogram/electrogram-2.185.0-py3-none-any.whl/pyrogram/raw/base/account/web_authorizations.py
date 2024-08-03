from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WebAuthorizations = Union["raw.types.account.WebAuthorizations"]


# noinspection PyRedeclaration
class WebAuthorizations:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.WebAuthorizations"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
