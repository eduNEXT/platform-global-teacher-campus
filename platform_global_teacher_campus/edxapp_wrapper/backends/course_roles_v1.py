"""
Backend about Course Roles.
"""
from common.djangoapps.student.models import CourseAccessRole  # pylint: disable=import-error
from common.djangoapps.student.roles import CourseStaffRole, GlobalStaff  # pylint: disable=import-error


def get_course_staff_role():
    return CourseStaffRole


def get_course_access_role():
    return CourseAccessRole


def get_global_staff():
    return GlobalStaff
