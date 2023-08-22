"""
Database models for platform_global_teacher_campus.
"""
from django.db import models

class ValidationBody(models.Model):
    id = models.AutoField(primary_key=True)
    validator = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    admin_notes = models.CharField(max_length=50)
    organizations = models.CharField(max_length=50)
