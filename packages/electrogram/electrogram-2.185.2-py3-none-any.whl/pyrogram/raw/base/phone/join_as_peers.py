from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

JoinAsPeers = Union["raw.types.phone.JoinAsPeers"]


# noinspection PyRedeclaration
class JoinAsPeers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.JoinAsPeers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
