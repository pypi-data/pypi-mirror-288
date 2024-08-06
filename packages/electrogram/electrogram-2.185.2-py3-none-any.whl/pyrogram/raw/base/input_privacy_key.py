from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPrivacyKey = Union["raw.types.InputPrivacyKeyAbout", "raw.types.InputPrivacyKeyAddedByPhone", "raw.types.InputPrivacyKeyBirthday", "raw.types.InputPrivacyKeyChatInvite", "raw.types.InputPrivacyKeyForwards", "raw.types.InputPrivacyKeyPhoneCall", "raw.types.InputPrivacyKeyPhoneNumber", "raw.types.InputPrivacyKeyPhoneP2P", "raw.types.InputPrivacyKeyProfilePhoto", "raw.types.InputPrivacyKeyStatusTimestamp", "raw.types.InputPrivacyKeyVoiceMessages"]


# noinspection PyRedeclaration
class InputPrivacyKey:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputPrivacyKey"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
