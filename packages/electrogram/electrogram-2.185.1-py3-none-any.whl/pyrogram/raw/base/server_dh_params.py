from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ServerDHParams = Union["raw.types.ServerDHParamsFail", "raw.types.ServerDHParamsOk"]


# noinspection PyRedeclaration
class ServerDHParams:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ServerDHParams"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
