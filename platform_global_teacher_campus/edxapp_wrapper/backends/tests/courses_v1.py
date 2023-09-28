"""
Backend for contenstore courses.
"""
from django.db import models


class CourseOverviewTestModel(models.Model):
    """
    Model for tests.
    """


def get_course_overview():
    """
    Gets course overview model from edxapp.
    """
    return CourseOverviewTestModel
