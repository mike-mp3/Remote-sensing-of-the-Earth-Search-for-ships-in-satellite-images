"""Models for country object."""


from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "Country",
    "CreateCountryCommand",
    "ReadCountryQuery",
    "UpdateCountryCommand",
    "DeleteCountryCommand",
]


class BaseCountry(BaseModel):
    """Base model for country."""


class CountryFields:
    id: PositiveInt = Field(description="Internal skill id.", examples=[1])
    name: str = Field(description="Country name.", examples=["Russia"])
    code: str = Field(description="Country code.", examples=["RUS"], pattern=r"^[A-Z]{3}$")


class _Country(BaseCountry):
    name: str = CountryFields.name
    code: str = CountryFields.code


class Country(_Country):
    id: PositiveInt = CountryFields.id


# Commands.
class CreateCountryCommand(_Country):
    ...


class UpdateCountryCommand(_Country):
    id: PositiveInt = CountryFields.id


class DeleteCountryCommand(BaseCountry):
    id: PositiveInt = CountryFields.id


# Queries.
class ReadCountryQuery(BaseCountry):
    id: PositiveInt = CountryFields.id
