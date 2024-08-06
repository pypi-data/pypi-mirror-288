from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ShippingOption = Union["raw.types.ShippingOption"]


# noinspection PyRedeclaration
class ShippingOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ShippingOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
