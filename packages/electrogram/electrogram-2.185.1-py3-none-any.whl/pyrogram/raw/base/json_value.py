from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

JSONValue = Union["raw.types.JsonArray", "raw.types.JsonBool", "raw.types.JsonNull", "raw.types.JsonNumber", "raw.types.JsonObject", "raw.types.JsonString"]


# noinspection PyRedeclaration
class JSONValue:  # type: ignore
    QUALNAME = "pyrogram.raw.base.JSONValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
