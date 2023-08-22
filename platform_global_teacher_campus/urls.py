"""
URLs for platform_global_teacher_campus.
"""
from django.urls import re_path  # pylint: disable=unused-import
from django.views.generic import TemplateView  # pylint: disable=unused-import
from platform_global_teacher_campus.views import ValidationBodyViewSet
from django.conf.urls import url

urlpatterns = [
    url(r'^validation_body/$', ValidationBodyViewSet.as_view(), name='validation_body'),
]
