"""
Backend for contenstore courses.
"""
from typing import Any
from django.db import models


class CourseOverviewTestModel(models.Model):
    """
    Model for tests.
    """
    def __init__(self, course_id) -> None:
        self.course_id = course_id
        super().__init__()


def get_course_overview():
    """
    Gets course overview model from edxapp.
    """
    return CourseOverviewTestModel
