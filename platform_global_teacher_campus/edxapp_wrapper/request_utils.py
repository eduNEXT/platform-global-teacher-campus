"""
Get models and functions from request_utils.
"""

from importlib import import_module

from django.conf import settings


def get_course_id_from_url():
    """ Gets the course_id_from_url function. """

    backend_function = settings.REQUEST_UTILS_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_id_from_url()
