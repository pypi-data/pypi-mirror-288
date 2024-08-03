from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ExportedInvoice = Union["raw.types.payments.ExportedInvoice"]


# noinspection PyRedeclaration
class ExportedInvoice:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.ExportedInvoice"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
