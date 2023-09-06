"""
Backend for Force Publish Course Command.
"""

from cms.djangoapps.contentstore.management.commands.utils import get_course_versions
from xmodule.modulestore.split_mongo.split_draft import DraftVersioningModuleStore
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.mixed import MixedModuleStore
from opaque_keys.edx.keys import CourseKey


def get_force_publish_course_command():
    """
    Gets force publish course command class from edxapp.
    """

    return DraftVersioningModuleStore

def get_course_versions_branches():
    """
    Gets force publish course command class from edxapp.
    """

    return get_course_versions

def get_modulestore():
    """
    Gets the UserAttribute model.
    """

    return modulestore

def get_course_key():
    """
    Gets the CourseKey model.
    """

    return CourseKey

def get_mixed_module_store():
    """
    Gets the CourseKey model.
    """

    return MixedModuleStore
