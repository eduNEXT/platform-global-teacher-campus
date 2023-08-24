""" urls.py """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from platform_global_teacher_campus.api.v1 import views

app_name = 'platform_global_teacher_campus'

router = DefaultRouter()
router.register(r'course-category', views.CourseCategoryViewSet)
router.register(r'validation-body', views.ValidationBodyViewSet)

urlpatterns = [
    path('', include((router.urls, app_name), namespace="pgtc-api")),
]
