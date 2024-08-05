from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

NewSession = Union["raw.types.NewSessionCreated"]


# noinspection PyRedeclaration
class NewSession:  # type: ignore
    QUALNAME = "pyrogram.raw.base.NewSession"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
