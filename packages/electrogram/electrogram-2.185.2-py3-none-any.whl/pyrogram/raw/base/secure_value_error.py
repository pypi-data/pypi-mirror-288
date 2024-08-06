from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SecureValueError = Union["raw.types.SecureValueError", "raw.types.SecureValueErrorData", "raw.types.SecureValueErrorFile", "raw.types.SecureValueErrorFiles", "raw.types.SecureValueErrorFrontSide", "raw.types.SecureValueErrorReverseSide", "raw.types.SecureValueErrorSelfie", "raw.types.SecureValueErrorTranslationFile", "raw.types.SecureValueErrorTranslationFiles"]


# noinspection PyRedeclaration
class SecureValueError:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SecureValueError"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
