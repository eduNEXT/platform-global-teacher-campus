"""
Backend for contenstore courses.
"""

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error


def get_course_overview():
    """
    Gets course overview model from edxapp.
    """
    return CourseOverview
