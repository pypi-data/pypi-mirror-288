from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Authorizations = Union["raw.types.account.Authorizations"]


# noinspection PyRedeclaration
class Authorizations:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.Authorizations"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
