from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPrivacyRule = Union["raw.types.InputPrivacyValueAllowAll", "raw.types.InputPrivacyValueAllowChatParticipants", "raw.types.InputPrivacyValueAllowCloseFriends", "raw.types.InputPrivacyValueAllowContacts", "raw.types.InputPrivacyValueAllowPremium", "raw.types.InputPrivacyValueAllowUsers", "raw.types.InputPrivacyValueDisallowAll", "raw.types.InputPrivacyValueDisallowChatParticipants", "raw.types.InputPrivacyValueDisallowContacts", "raw.types.InputPrivacyValueDisallowUsers"]


# noinspection PyRedeclaration
class InputPrivacyRule:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputPrivacyRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
