"""
Backend for contenstore courses.
"""

from cms.djangoapps.contentstore.views.course import (  # pylint: disable=import-error
    _process_courses_list,
    get_courses_accessible_to_user,
)
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error
from openedx.core.djangoapps.models.course_details import CourseDetails  # pylint: disable=import-error

def get_course_overview():
    """
    Gets course overview model from edxapp.
    """
    return CourseOverview
