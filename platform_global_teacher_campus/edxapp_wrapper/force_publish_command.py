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

def get_course_versions_branches():
    """ Gets get_course_versions from commands utils. """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_versions_branches()

def get_modulestore():
    """ Gets the UserAttribute. """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_modulestore()

def get_course_key():
    """ Gets the CourseKey. """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_key()

def get_mixed_module_store():
    """ Gets the MixedModuleStore. """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_mixed_module_store()
