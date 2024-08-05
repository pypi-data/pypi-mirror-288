from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DeepLinkInfo = Union["raw.types.help.DeepLinkInfo", "raw.types.help.DeepLinkInfoEmpty"]


# noinspection PyRedeclaration
class DeepLinkInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.DeepLinkInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
