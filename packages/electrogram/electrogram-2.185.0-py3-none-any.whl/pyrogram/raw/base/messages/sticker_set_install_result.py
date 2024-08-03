from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StickerSetInstallResult = Union["raw.types.messages.StickerSetInstallResultArchive", "raw.types.messages.StickerSetInstallResultSuccess"]


# noinspection PyRedeclaration
class StickerSetInstallResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.StickerSetInstallResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
