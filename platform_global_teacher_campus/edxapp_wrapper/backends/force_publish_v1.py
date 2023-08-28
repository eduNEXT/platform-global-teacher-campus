"""
Backend for Force Publish Course.
"""

from cms.djangoapps.maintenance.views import ForcePublishCourseRenderStarted

def get_force_publish_course():
    """
    Gets force publish course class from edxapp.
    """

    return ForcePublishCourseRenderStarted
