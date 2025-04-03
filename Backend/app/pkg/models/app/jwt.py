from pydantic import Field

__all__ = [
    "JWTFields"
]

class JWTFields:
    access_token = Field(
        description="Access token",
        example="exam.ple.token",
    )
    refresh_token = Field(
        description="Refresh token",
        example="exam.ple.token",
    )
