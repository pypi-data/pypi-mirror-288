from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

NotificationSound = Union["raw.types.NotificationSoundDefault", "raw.types.NotificationSoundLocal", "raw.types.NotificationSoundNone", "raw.types.NotificationSoundRingtone"]


# noinspection PyRedeclaration
class NotificationSound:  # type: ignore
    QUALNAME = "pyrogram.raw.base.NotificationSound"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
