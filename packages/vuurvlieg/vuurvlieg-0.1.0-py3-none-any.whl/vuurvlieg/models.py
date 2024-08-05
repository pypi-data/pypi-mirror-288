"""Models for Firefly."""

from __future__ import annotations


from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class AboutResponse(DataClassORJSONMixin):
    """AboutResponse model."""

    data: About


@dataclass
class About(DataClassORJSONMixin):
    """About model."""

    version: str
    api_version: str
    php_version: str
    os: str
    driver: str
