from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PrivacyRule = Union["raw.types.PrivacyValueAllowAll", "raw.types.PrivacyValueAllowChatParticipants", "raw.types.PrivacyValueAllowCloseFriends", "raw.types.PrivacyValueAllowContacts", "raw.types.PrivacyValueAllowPremium", "raw.types.PrivacyValueAllowUsers", "raw.types.PrivacyValueDisallowAll", "raw.types.PrivacyValueDisallowChatParticipants", "raw.types.PrivacyValueDisallowContacts", "raw.types.PrivacyValueDisallowUsers"]


# noinspection PyRedeclaration
class PrivacyRule:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PrivacyRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
