""" urls.py """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from platform_global_teacher_campus.api.v1 import views

app_name = 'platform_global_teacher_campus'

router = DefaultRouter()
router.register(r'course-category', views.CourseCategoryViewSet)
router.register(r'validation-body', views.ValidationBodyViewSet)
router.register(r'validation-process', views.ValidationProcessViewSet)
router.register(r'validation-process-event', views.ValidationProcessEventViewSet)

urlpatterns = [
    path('', include((router.urls, app_name), namespace="pgtc-api")),
    path('validation-processes/<str:course_id>/submit/', views.submit_validation_process, name="validation-process-submit"),
]
