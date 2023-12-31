"""
Backend for Force Publish Course Command.
"""

from cms.djangoapps.contentstore.management.commands.utils import get_course_versions  # pylint: disable=import-error
from xmodule.modulestore.django import modulestore  # pylint: disable=import-error
from xmodule.modulestore.mixed import MixedModuleStore  # pylint: disable=import-error
from xmodule.modulestore.split_mongo.split_draft import DraftVersioningModuleStore  # pylint: disable=import-error


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


def get_mixed_module_store():
    """
    Gets ModuleStore knows how to route requests to the right persistence ms.
    """

    return MixedModuleStore
