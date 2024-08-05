from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WallPapers = Union["raw.types.account.WallPapers", "raw.types.account.WallPapersNotModified"]


# noinspection PyRedeclaration
class WallPapers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.WallPapers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
