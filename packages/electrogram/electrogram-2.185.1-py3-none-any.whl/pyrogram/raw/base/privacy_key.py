from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PrivacyKey = Union["raw.types.PrivacyKeyAbout", "raw.types.PrivacyKeyAddedByPhone", "raw.types.PrivacyKeyBirthday", "raw.types.PrivacyKeyChatInvite", "raw.types.PrivacyKeyForwards", "raw.types.PrivacyKeyPhoneCall", "raw.types.PrivacyKeyPhoneNumber", "raw.types.PrivacyKeyPhoneP2P", "raw.types.PrivacyKeyProfilePhoto", "raw.types.PrivacyKeyStatusTimestamp", "raw.types.PrivacyKeyVoiceMessages"]


# noinspection PyRedeclaration
class PrivacyKey:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PrivacyKey"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
