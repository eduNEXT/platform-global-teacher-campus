"""
Backend for contenstore courses.
"""
from django.db import models


class CourseOverviewTestModel(models.Model):
    """
    Model for tests.
    """
    def __init__(self, id, org=None) -> None:
        self.id = id
        self.org = org
        super().__init__()


def get_course_overview():
    """
    Gets course overview model from edxapp.
    """
    return CourseOverviewTestModel
