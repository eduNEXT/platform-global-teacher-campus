"""
Backend for Force Publish Course.
"""

from cms.djangoapps.maintenance.views import ForcePublishCourseRenderStarted  # pylint: disable=import-error


def get_force_publish_course():
    """
    Gets force publish course class from edxapp.
    """

    return ForcePublishCourseRenderStarted
