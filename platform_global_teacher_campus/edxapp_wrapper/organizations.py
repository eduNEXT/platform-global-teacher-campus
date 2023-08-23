"""
Organizations definitions.
"""

from importlib import import_module

from django.conf import settings

def get_organization_model():
    """ Gets the organizations model from edxapp. """

    backend_function = settings.ORGANIZATIONS_BACKEND
    backend = import_module(backend_function)

    return backend.get_organization_model()
