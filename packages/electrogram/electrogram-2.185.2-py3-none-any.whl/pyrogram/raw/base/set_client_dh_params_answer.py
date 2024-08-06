from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SetClientDHParamsAnswer = Union["raw.types.DhGenFail", "raw.types.DhGenOk", "raw.types.DhGenRetry"]


# noinspection PyRedeclaration
class SetClientDHParamsAnswer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SetClientDHParamsAnswer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
