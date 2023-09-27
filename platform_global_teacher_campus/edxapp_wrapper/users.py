"""
Courses definitions.
"""

from importlib import import_module

from django.conf import settings


def get_user_model():
    """ Gets the course overview model from edxapp. """

    backend_function = settings.USER_MODEL_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_model()
