"""
Force publish course command definitions.
"""

from importlib import import_module

from django.conf import settings

def get_force_publish_course_command():
    """ Gets force publish course command class from edxapp. """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_force_publish_course_command()
