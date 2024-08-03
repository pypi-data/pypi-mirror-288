from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReactionNotificationsFrom = Union["raw.types.ReactionNotificationsFromAll", "raw.types.ReactionNotificationsFromContacts"]


# noinspection PyRedeclaration
class ReactionNotificationsFrom:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReactionNotificationsFrom"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
