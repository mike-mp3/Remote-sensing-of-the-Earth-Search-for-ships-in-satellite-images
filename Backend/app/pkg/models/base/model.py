"""Base model for all models in API server."""

from __future__ import annotations

import time
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import UUID

import pydantic
from pydantic import UUID4, ConfigDict

from app.pkg.models import types

__all__ = ["BaseModel", "Model"]

Model = TypeVar("Model", bound="BaseModel")
_T = TypeVar("_T")


class BaseModel(pydantic.BaseModel):
    """Base model for all models in API server."""


    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        json_encoders = {
            pydantic.SecretStr: lambda v: v.get_secret_value() if v else None,
            pydantic.SecretBytes: lambda v: v.get_secret_value() if v else None,
            bytes: lambda v: v.decode() if v else None,
            datetime: lambda v: int(v.timestamp()) if v else None,
            date: lambda v: int(time.mktime(v.timetuple())) if v else None,
        }
    )

    def to_dict(
        self,
        show_secrets: bool = False,
        values: dict[Any, Any] = None,
        **kwargs,
    ) -> dict[Any, Any]:
        """Make a representation model from a class object to Dict object.

        Args:
            show_secrets:
                bool.
                default False.
                Shows secret in dict an object if True.
            values:
                Using an object to write to a Dict object.
            **kwargs:
                Optional arguments to be passed to the Dict object.

        Examples:
            If you don't want to show secret in a dict object,
            then you shouldn't use ``show_secrets`` argument::

                >>> from app.pkg.models.base import BaseModel
                >>> class TestModel(BaseModel):
                ...     some_value: pydantic.SecretStr
                ...     some_value_two: pydantic.SecretBytes
                >>> model = TestModel(some_value="key", some_value_two="value")
                >>> assert isinstance(model.some_value, pydantic.SecretStr)
                >>> assert isinstance(model.some_value_two, pydantic.SecretBytes)
                >>> dict_model = model.to_dict()
                >>> assert isinstance(dict_model["some_value"], str)
                >>> assert isinstance(dict_model["some_value_two"], str)
                >>> print(dict_model["some_value"])
                '**********'
                >>> print(dict_model["some_value_two"])
                '**********'

            If you want to deciphe sensitivity in a dict object,
            then you should use ``show_secrets`` argument::

                >>> from app.pkg.models.base import BaseModel
                >>> class TestModel(BaseModel):
                ...     some_value: pydantic.SecretStr
                ...     some_value_two: pydantic.SecretBytes
                >>> model = TestModel(some_value="key", some_value_two="value")
                >>> assert isinstance(model.some_value, pydantic.SecretStr)
                >>> assert isinstance(model.some_value_two, pydantic.SecretBytes)
                >>> dict_model = model.to_dict(show_secrets=True)
                >>> assert isinstance(dict_model["some_value"], str)
                >>> assert isinstance(dict_model["some_value_two"], str)
                >>> print(dict_model["some_value"])
                'key'
                >>> print(dict_model["some_value_two"])
                'value'

            In such cases, you can use the ``values`` argument for revrite values in
            a dict object::

                >>> from app.pkg.models.base import BaseModel
                >>> class TestModel(BaseModel):
                ...     some_value: pydantic.SecretStr
                ...     some_value_two: pydantic.SecretBytes
                >>> model = TestModel(some_value="key", some_value_two="value")
                >>> assert isinstance(model.some_value, pydantic.SecretStr)
                >>> assert isinstance(model.some_value_two, pydantic.SecretBytes)
                >>> dict_model = model.to_dict(
                ...     show_secrets=True,
                ...     values={"some_value": "value"}
                ... )
                >>> assert isinstance(dict_model["some_value"], str)
                >>> assert isinstance(dict_model["some_value_two"], str)
                >>> print(dict_model["some_value"])
                'value'
                >>> print(dict_model["some_value_two"])
                'value'

        Raises:
            TypeError: If ``values`` are not a Dict object.

        Returns:
            Dict object with reveal password filed.
        """

        values = self.model_dump(**kwargs).items() if not values else values.items()
        r = {}
        for k, v in values:
            v = self.__cast_values(v=v, show_secrets=show_secrets)
            r[k] = v
        return r

    def __cast_values(self, v: _T, show_secrets: bool, **kwargs) -> _T:
        """Cast value for dict object.

        Args:
            v:
                Any value.
            show_secrets:
                If True, then the secret will be revealed.

        Warnings:
            This method is not memory optimized.
        """

        if isinstance(v, (List, Tuple)):
            return [
                self.__cast_values(v=ve, show_secrets=show_secrets, **kwargs)
                for ve in v
            ]

        elif isinstance(v, (pydantic.SecretBytes, pydantic.SecretStr)):
            return self.__cast_secret(v=v, show_secrets=show_secrets)

        elif isinstance(v, Dict) and v:
            return self.to_dict(show_secrets=show_secrets, values=v, **kwargs)

        elif isinstance(v, UUID):
            return str(v)

        elif isinstance(v, datetime):
            return v.timestamp()

        return v

    @staticmethod
    def __cast_secret(v, show_secrets: bool) -> str:
        """Cast secret value to str.

        Args:
            v: pydantic.Secret* object.
            show_secrets: bool value. If True, then the secret will be revealed.

        Returns: str value of ``v``.
        """

        if isinstance(v, pydantic.SecretBytes):
            return v.get_secret_value().decode() if show_secrets else str(v)
        elif isinstance(v, pydantic.SecretStr):
            return v.get_secret_value() if show_secrets else str(v)

    def delete_attribute(self, attr: str) -> BaseModel:
        """Delete some attribute field from a model.

        Args:
            attr:
                name of field.

        Returns:
            self object.
        """

        delattr(self, attr)
        return self
