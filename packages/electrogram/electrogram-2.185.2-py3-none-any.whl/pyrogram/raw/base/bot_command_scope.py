from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotCommandScope = Union["raw.types.BotCommandScopeChatAdmins", "raw.types.BotCommandScopeChats", "raw.types.BotCommandScopeDefault", "raw.types.BotCommandScopePeer", "raw.types.BotCommandScopePeerAdmins", "raw.types.BotCommandScopePeerUser", "raw.types.BotCommandScopeUsers"]


# noinspection PyRedeclaration
class BotCommandScope:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BotCommandScope"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
