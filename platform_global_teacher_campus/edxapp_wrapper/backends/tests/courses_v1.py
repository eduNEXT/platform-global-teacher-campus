"""
Backend for contenstore courses.
"""

from django.db import models


class CourseOverviewTestModel(models.Model):
    """
    Model for tests.
    """
    id = models.CharField(primary_key=True, max_length=100)
    org = models.CharField(max_length=100)  # Adjust the field as needed
    display_name = models.CharField(max_length=100)


def get_course_overview():
    """
    Gets course overview model from edxapp.
    """
    return CourseOverviewTestModel
