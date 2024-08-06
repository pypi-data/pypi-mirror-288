from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputInvoice = Union["raw.types.InputInvoiceMessage", "raw.types.InputInvoicePremiumGiftCode", "raw.types.InputInvoiceSlug", "raw.types.InputInvoiceStars"]


# noinspection PyRedeclaration
class InputInvoice:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputInvoice"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
