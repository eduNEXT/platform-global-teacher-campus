"""
Database models for platform_global_teacher_campus.
"""

from django.db import models

class CourseCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    #parentCategory = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    parentCategory = models.IntegerField()

    def __str__(self):
        return self.name

class ValidationProcess(models.Model):
    id = models.AutoField(primary_key=True)
    courseId = models.IntegerField()
    categories = models.ManyToManyField(CourseCategory)
    organizationId = models.IntegerField()
    currentValidationUserId = models.IntegerField()
    validationBodyId = models.IntegerField()

    def __str__(self):
        return f"Validation Process for Course {self.courseid}"