"""Asynchronous Python client for Firefly."""


class FireflyError(Exception):
    """Generic exception."""


class FireflyConnectionError(FireflyError):
    """Firefly connection exception."""
