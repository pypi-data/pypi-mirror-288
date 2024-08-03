from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SponsoredMessageReportResult = Union["raw.types.channels.SponsoredMessageReportResultAdsHidden", "raw.types.channels.SponsoredMessageReportResultChooseOption", "raw.types.channels.SponsoredMessageReportResultReported"]


# noinspection PyRedeclaration
class SponsoredMessageReportResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.channels.SponsoredMessageReportResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
