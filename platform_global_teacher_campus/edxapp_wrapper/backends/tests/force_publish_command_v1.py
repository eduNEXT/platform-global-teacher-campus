"""
Backend for Force Publish Course Command.
"""

from unittest.mock import MagicMock


def get_force_publish_course_command():
    """
    Gets helper method to forcefully publish a course,
    making the published branch point to the same structure as the draft branch.
    """

    return MagicMock


def get_course_versions_branches():
    """
    Gets fetches the latest course versions.
    """

    return MagicMock


def get_modulestore():
    """
    Gets a modulestore wrapper.
    """

    return MagicMock


def get_mixed_module_store():
    """
    Gets ModuleStore knows how to route requests to the right persistence ms.
    """

    return MagicMock
