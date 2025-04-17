import enum

from fastapi import status

__all__ = ["Mapper"]


class WSCode(enum.IntEnum):
    NORMAL_CLOSURE = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA = 1003
    NO_STATUS_RECEIVED = 1005
    ABNORMAL_CLOSURE = 1006
    INVALID_FRAME_PAYLOAD_DATA = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MANDATORY_EXTENSION = 1010
    INTERNAL_ERROR = 1011
    SERVICE_RESTART = 1012
    TRY_AGAIN_LATER = 1013
    BAD_GATEWAY = 1014
    TLS_HANDSHAKE = 1015
    UNAUTHORIZED = 3000
    FORBIDDEN = 3003
    TIMEOUT = 3008


class Mapper:
    mapper = {
        status.HTTP_401_UNAUTHORIZED: WSCode.UNAUTHORIZED,
        status.HTTP_500_INTERNAL_SERVER_ERROR: WSCode.INTERNAL_ERROR,
    }

    @classmethod
    def map_http_to_ws(cls, http_status: int) -> int:
        try:
            return cls.mapper[http_status]
        except KeyError:
            return WSCode.INTERNAL_ERROR
