"""
Force publish definitions.
"""

from importlib import import_module

from django.conf import settings

def get_modulestore():
    """ Gets the UserAttribute model """
    backend_function = settings.PUBLISH_BACKEND
    backend = import_module(backend_function)

    return backend.get_modulestore()

def get_get_xblock():
    """ Gets the UserAttribute model """
    backend_function = settings.PUBLISH_BACKEND
    backend = import_module(backend_function)

    return backend.get_get_xblock()

def get_usage_key_with_run():
    """ Gets the UserAttribute model """
    backend_function = settings.PUBLISH_BACKEND
    backend = import_module(backend_function)

    return backend.get_usage_key_with_run()
