from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RpcError = Union["raw.types.RpcError"]


# noinspection PyRedeclaration
class RpcError:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RpcError"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
