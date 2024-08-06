from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

IpPort = Union["raw.types.IpPort", "raw.types.IpPortSecret"]


# noinspection PyRedeclaration
class IpPort:  # type: ignore
    QUALNAME = "pyrogram.raw.base.IpPort"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
