from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

UserProfilePhoto = Union["raw.types.UserProfilePhoto", "raw.types.UserProfilePhotoEmpty"]


# noinspection PyRedeclaration
class UserProfilePhoto:  # type: ignore
    QUALNAME = "pyrogram.raw.base.UserProfilePhoto"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
