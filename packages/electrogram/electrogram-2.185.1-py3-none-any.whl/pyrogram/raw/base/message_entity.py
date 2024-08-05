from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageEntity = Union["raw.types.InputMessageEntityMentionName", "raw.types.MessageEntityBankCard", "raw.types.MessageEntityBlockquote", "raw.types.MessageEntityBold", "raw.types.MessageEntityBotCommand", "raw.types.MessageEntityCashtag", "raw.types.MessageEntityCode", "raw.types.MessageEntityCustomEmoji", "raw.types.MessageEntityEmail", "raw.types.MessageEntityHashtag", "raw.types.MessageEntityItalic", "raw.types.MessageEntityMention", "raw.types.MessageEntityMentionName", "raw.types.MessageEntityPhone", "raw.types.MessageEntityPre", "raw.types.MessageEntitySpoiler", "raw.types.MessageEntityStrike", "raw.types.MessageEntityTextUrl", "raw.types.MessageEntityUnderline", "raw.types.MessageEntityUnknown", "raw.types.MessageEntityUrl"]


# noinspection PyRedeclaration
class MessageEntity:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageEntity"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
