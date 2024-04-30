"""
Django command to wait for the database to be available.
"""

from typing import Any
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Wait for the database"""

    def handle(self, *args: Any, **options: Any) -> str | None:
        return super().handle(*args, **options)
