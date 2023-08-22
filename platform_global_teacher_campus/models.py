"""
Database models for platform_global_teacher_campus.
"""

from django.db import models
from edxapp_wrapper.courses import get_course_overview

CourseOverview=get_course_overview()
class CourseCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parentCategory = models.IntegerField()

    def __str__(self):
        return self.name

class ValidationProcess(models.Model):
    id = models.AutoField(primary_key=True)
    courseId = models.ForeignKey(CourseOverview, on_delete=models.CASCADE)
    categories = models.ManyToManyField(CourseCategory)
    organizationId = models.IntegerField()
    currentValidationUserId = models.IntegerField()
    validationBodyId = models.IntegerField()

    def __str__(self):
        return f"Validation Process for Course {self.courseid}"