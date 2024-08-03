from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SponsoredMessageReportOption = Union["raw.types.SponsoredMessageReportOption"]


# noinspection PyRedeclaration
class SponsoredMessageReportOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SponsoredMessageReportOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
