from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPhoneCall = Union["raw.types.InputPhoneCall"]


# noinspection PyRedeclaration
class InputPhoneCall:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputPhoneCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
