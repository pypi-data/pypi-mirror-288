from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedStoryLink = Union["raw.types.ExportedStoryLink"]


# noinspection PyRedeclaration
class ExportedStoryLink:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ExportedStoryLink"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
