from typing import Dict, Optional, Union, Any
from pydantic import SecretStr

from app.pkg.models import ActiveUser

__all__ = ["JwtAuthorizationCredentials"]


class JwtAuthorizationCredentials:
    subject: Dict[str, Any]
    raw_token: SecretStr
    jti: Optional[str]

    def __init__(
        self,
        subject: Dict[str, Dict[str, Any]],
        raw_token: SecretStr,
        jti: Optional[str] = None,
    ):
        self.subject = subject
        self.jti = jti
        self.raw_token = raw_token

    def __getitem__(self, item: str) -> Union[str, int]:
        return self.subject[item]

    def get_user(self) -> ActiveUser:
        return ActiveUser(
            id=self.subject.get("user_id"),
            email=self.subject.get("email"),
            role_name=self.subject.get("role_name"),
            is_activated=self.subject.get("is_activated"),
        )
