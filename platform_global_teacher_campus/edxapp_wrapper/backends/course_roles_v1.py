from common.djangoapps.student.models import CourseAccessRole
from common.djangoapps.student.roles import CourseStaffRole, GlobalStaff


def get_course_staff_role():
    return CourseStaffRole

def get_course_access_role():
    return CourseAccessRole

def get_global_staff():
    return GlobalStaff
