"""
Database models for platform_global_teacher_campus.
"""

from django.db import models
from django import forms
from edxapp_wrapper.courses import get_course_overview

CourseOverview=get_course_overview()

class CourseCategory(models.Model):
    name = models.CharField()
    parentCategory = models.IntegerField()

    def __str__(self):
        return self.name


class ValidationProcess(models.Model):
    courseId = models.OneToOneField(CourseOverview, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(CourseCategory)
    organizationId = models.IntegerField()
    currentValidationUserId = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)
    validationBodyId = models.ForeignKey(ValidationBody, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Validation Process for Course {self.courseid}"


class ValidationBody(models.Model):
    validators = models.ManyToManyField('Users')
    name = models.CharField()
    adminNotes = models.CharField()
    organizations = models.ManyToManyField('Organizations')


class ValidationProcessEvent(models.Model):
    validationProcessId = models.ForeignKey(ValidationProcess, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    status = forms.ChoiceField()
    comment = models.TextField()
    userId = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)
    reasonId = models.ForeignKey(ValidationRejectionReason, on_delete=models.SET_NULL, null=True)


class ValidationRejectionReason(models.Model):
    name = models.CharField()


class ValidationRules(models.Model):
    userId = models.OneToOneField(ValidationBody)
    validationBodyId = models.IntegerField()
    type = forms.ChoiceField()
    adminNotes = models.TextField
    organizationId = models.IntegerField()
    is_active = models.BooleanField()
