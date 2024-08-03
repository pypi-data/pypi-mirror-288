from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ResolvedBusinessChatLinks = Union["raw.types.account.ResolvedBusinessChatLinks"]


# noinspection PyRedeclaration
class ResolvedBusinessChatLinks:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.ResolvedBusinessChatLinks"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
