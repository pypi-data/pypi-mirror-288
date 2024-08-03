from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ConnectedBots = Union["raw.types.account.ConnectedBots"]


# noinspection PyRedeclaration
class ConnectedBots:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.ConnectedBots"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
