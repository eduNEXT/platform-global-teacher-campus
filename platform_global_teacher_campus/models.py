"""
Database models for platform_global_teacher_campus.
"""

from django.db import models
from django import forms
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.edxapp_wrapper.users import get_user_model
from platform_global_teacher_campus.edxapp_wrapper.organizations import get_organization_model

CourseOverview = get_course_overview()
User = get_user_model()
Organization = get_organization_model()


class CourseCategory(models.Model):
    name = models.TextField()
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class ValidationBody(models.Model):
    validators = models.ManyToManyField(User)
    name = models.TextField()
    admin_notes = models.TextField(default="")
    organizations = models.ManyToManyField(Organization)


class ValidationProcess(models.Model):
    course = models.OneToOneField(CourseOverview, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(CourseCategory)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    current_validation_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    validation_body = models.ForeignKey(ValidationBody, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Validation Process for Course {self.courseid}"


class ValidationRejectionReason(models.Model):
    name = models.TextField()


class ValidationProcessEvent(models.Model):
    validation_process = models.ForeignKey(ValidationProcess, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    status = forms.ChoiceField() # ToDo: add list
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.ForeignKey(ValidationRejectionReason, on_delete=models.SET_NULL, null=True, blank=True)


class ValidationRules(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    validation_body = models.ForeignKey(ValidationBody, on_delete=models.CASCADE, null=True, blank=True)
    permission_type = forms.ChoiceField()
    admin_notes = models.TextField(default="")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField()
