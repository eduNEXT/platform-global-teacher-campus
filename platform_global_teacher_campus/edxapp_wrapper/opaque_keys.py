"""
Get models and functions from opaque_keys.
"""

from importlib import import_module

from django.conf import settings

def get_usage_key():
    """ Gets the usage_key from opaque_key package. """

    backend_function = settings.OPAQUE_KEY_BACKEND
    backend = import_module(backend_function)

    return backend.get_usage_key()
