""" urls.py """

from django.urls import include, path

app_name = 'platform_global_teacher_campus'  # pylint: disable=invalid-name

urlpatterns = [  # pylint: disable=invalid-name
    path('v1/', include('platform_global_teacher_campus.api.v1.urls', namespace='api-v1')),
]
