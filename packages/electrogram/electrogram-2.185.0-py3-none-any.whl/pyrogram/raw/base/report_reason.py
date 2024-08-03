from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReportReason = Union["raw.types.InputReportReasonChildAbuse", "raw.types.InputReportReasonCopyright", "raw.types.InputReportReasonFake", "raw.types.InputReportReasonGeoIrrelevant", "raw.types.InputReportReasonIllegalDrugs", "raw.types.InputReportReasonOther", "raw.types.InputReportReasonPersonalDetails", "raw.types.InputReportReasonPornography", "raw.types.InputReportReasonSpam", "raw.types.InputReportReasonViolence"]


# noinspection PyRedeclaration
class ReportReason:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReportReason"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
