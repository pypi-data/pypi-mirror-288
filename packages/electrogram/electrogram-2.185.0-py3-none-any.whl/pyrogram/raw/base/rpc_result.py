from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RpcResult = Union["raw.types.RpcResult"]


# noinspection PyRedeclaration
class RpcResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RpcResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
