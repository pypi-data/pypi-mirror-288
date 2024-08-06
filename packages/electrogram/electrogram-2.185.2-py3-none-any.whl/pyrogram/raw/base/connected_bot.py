from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ConnectedBot = Union["raw.types.ConnectedBot"]


# noinspection PyRedeclaration
class ConnectedBot:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ConnectedBot"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
