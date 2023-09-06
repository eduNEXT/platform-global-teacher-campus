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
    Gets helper method to forcefully publish a course,
    making the published branch point to the same structure as the draft branch.
    """

    return DraftVersioningModuleStore

def get_course_versions_branches():
    """
    Gets fetches the latest course versions.
    """

    return get_course_versions

def get_modulestore():
    """
    Gets a modulestore wrapper.
    """

    return modulestore

def get_course_key():
    """
    Gets the CourseKey model.
    """

    return CourseKey

def get_mixed_module_store():
    """
    Gets ModuleStore knows how to route requests to the right persistence ms.
    """

    return MixedModuleStore
