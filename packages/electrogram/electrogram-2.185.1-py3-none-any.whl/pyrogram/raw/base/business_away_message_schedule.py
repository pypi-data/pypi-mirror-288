from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessAwayMessageSchedule = Union["raw.types.BusinessAwayMessageScheduleAlways", "raw.types.BusinessAwayMessageScheduleCustom", "raw.types.BusinessAwayMessageScheduleOutsideWorkHours"]


# noinspection PyRedeclaration
class BusinessAwayMessageSchedule:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessAwayMessageSchedule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
