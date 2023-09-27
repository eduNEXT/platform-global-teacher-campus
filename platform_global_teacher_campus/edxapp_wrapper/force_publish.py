"""
Force publish definitions.
"""

from importlib import import_module

from django.conf import settings


def get_force_publish_course():
    """ Gets force publish course class from edxapp. """

    backend_function = settings.FORCE_PUBLISH_BACKEND
    backend = import_module(backend_function)

    return backend.get_force_publish_course()
