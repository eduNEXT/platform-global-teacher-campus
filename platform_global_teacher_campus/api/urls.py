""" urls.py """

from django.urls import include, path

app_name = 'platform_global_teacher_campus'

urlpatterns = [
    path('v1/', include(('platform_global_teacher_campus.api.v1.urls', app_name), namespace="pgtc-api")),
]
