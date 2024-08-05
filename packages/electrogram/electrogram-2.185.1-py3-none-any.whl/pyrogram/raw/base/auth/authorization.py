from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Authorization = Union["raw.types.auth.Authorization", "raw.types.auth.AuthorizationSignUpRequired"]


# noinspection PyRedeclaration
class Authorization:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.Authorization"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
