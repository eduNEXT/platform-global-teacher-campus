"""
URLs for platform_global_teacher_campus.
"""
from django.urls import include, path

app_name = 'platform_global_teacher_campus'

urlpatterns = [
    path('api/', include(('platform_global_teacher_campus.api.urls', app_name), namespace="pgtc-api")),
]
