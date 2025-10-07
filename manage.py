#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from settings.config import ENV_ID, ENV_POSSIBLE_VALUES


def main():
    """Run administrative tasks."""
    assert ENV_ID in ENV_POSSIBLE_VALUES, f'ENV_ID must be one of {ENV_POSSIBLE_VALUES}'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{ENV_ID}')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
