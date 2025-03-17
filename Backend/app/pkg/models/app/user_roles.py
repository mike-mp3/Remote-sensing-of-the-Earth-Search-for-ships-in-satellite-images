from enum import IntEnum
from typing import Any
from pydantic_core import core_schema, CoreSchema
from pydantic import GetCoreSchemaHandler

__all__ = [
    "UserRoleID",
    "UserRoleName",
]

class UserRoleEnum(IntEnum):
    """General Enum for user roles"""
    ADMIN = 1
    DEFAULT = 2

# Custom types with validation
class UserRoleID(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            lambda v: UserRoleEnum(v), schema=core_schema.int_schema()
        )

class UserRoleName(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            lambda v: UserRoleEnum(v).name, schema=core_schema.str_schema()
        )
