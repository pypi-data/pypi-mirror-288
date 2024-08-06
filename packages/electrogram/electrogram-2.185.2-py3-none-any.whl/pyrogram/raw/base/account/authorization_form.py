from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AuthorizationForm = Union["raw.types.account.AuthorizationForm"]


# noinspection PyRedeclaration
class AuthorizationForm:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.AuthorizationForm"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
