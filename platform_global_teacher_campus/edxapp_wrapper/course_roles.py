"""
Courses definitions.
"""

from importlib import import_module

from django.conf import settings

def get_course_staff_role():
    """ Gets the course staff role model from edxapp. """

    backend_function = settings.COURSE_ROLE_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_staff_role()
