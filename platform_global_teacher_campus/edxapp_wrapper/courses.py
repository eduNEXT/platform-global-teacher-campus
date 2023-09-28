"""
Courses definitions.
"""

from importlib import import_module

from django.conf import settings


def get_course_overview():
    """ Gets the course overview model from edxapp. """

    backend_function = settings.CVW_COURSES_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_overview()
