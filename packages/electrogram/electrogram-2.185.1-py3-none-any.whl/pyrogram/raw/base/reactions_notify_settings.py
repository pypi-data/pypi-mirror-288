from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReactionsNotifySettings = Union["raw.types.ReactionsNotifySettings"]


# noinspection PyRedeclaration
class ReactionsNotifySettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReactionsNotifySettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
