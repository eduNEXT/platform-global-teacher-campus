"""
Backend for the create_edxapp_user that works under the open-release/lilac.master tag
"""
try:
    from xmodule.modulestore.django import modulestore
except:
    modulestore = None
try:
    from cms.djangoapps.contentstore.views.item import _get_xblock
except:
    _get_xblock = None
try:
    from cms.djangoapps.contentstore.views.helpers import usage_key_with_run
except:
    _get_xblock = None


def get_modulestore():
    """ Gets the UserAttribute model """
    return modulestore

def get_get_xblock():
    """ Gets the UserAttribute model """
    return _get_xblock

def get_usage_key_with_run():
    """H j."""
    return usage_key_with_run