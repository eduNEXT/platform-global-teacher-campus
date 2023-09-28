"""
Force publish course command definitions.
"""

from importlib import import_module

from django.conf import settings


def get_force_publish_course_command():
    """
    Gets helper method to forcefully publish a course,
    making the published branch point to the same structure as the draft branch.
    """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_force_publish_course_command()


def get_course_versions_branches():
    """
    Gets fetches the latest course versions.
    """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_versions_branches()


def get_modulestore():
    """
    Gets a modulestore wrapper.
    """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_modulestore()


def get_mixed_module_store():
    """
    Gets ModuleStore knows how to route requests to the right persistence ms.
    """

    backend_function = settings.FORCE_PUBLISH_COMMAND_BACKEND
    backend = import_module(backend_function)

    return backend.get_mixed_module_store()
