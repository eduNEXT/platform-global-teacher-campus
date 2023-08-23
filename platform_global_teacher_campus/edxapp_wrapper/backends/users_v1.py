"""
Backend for the create_edxapp_user that works under the open-release/lilac.master tag
"""
from django.contrib.auth import get_user_model as get_user_model_from_openedx


def get_user_model():
    """ Gets the UserAttribute model """
    return get_user_model_from_openedx()
