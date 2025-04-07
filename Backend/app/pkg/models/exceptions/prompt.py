from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "InvalidPromptPath",
    "RawPromptNowFound",
    "RawPromptAlreadyExists",
]

class InvalidPromptPath(BaseAPIException):
    message = "Invalid prompt path"
    status_code = status.HTTP_400_BAD_REQUEST

class RawPromptNowFound(BaseAPIException):
    message = "Raw prompt now not found. Try to upload again"
    status_code = status.HTTP_404_NOT_FOUND

class RawPromptAlreadyExists(BaseAPIException):
    message = (
        "Raw prompt already exists. "
        "Maybe, you need to get the new "
        "presigned link and upload image"
    )
    status_code = status.HTTP_409_CONFLICT