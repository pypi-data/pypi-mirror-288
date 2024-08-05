from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RpcDropAnswer = Union["raw.types.RpcAnswerDropped", "raw.types.RpcAnswerDroppedRunning", "raw.types.RpcAnswerUnknown"]


# noinspection PyRedeclaration
class RpcDropAnswer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RpcDropAnswer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
