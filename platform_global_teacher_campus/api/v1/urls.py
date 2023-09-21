""" urls.py """

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from platform_global_teacher_campus.api.v1 import views

app_name = 'platform_global_teacher_campus'

router = DefaultRouter()
router.register(r'categories', views.CourseCategoryViewSet)
router.register(r'validation-bodies', views.ValidationBodyViewSet)

urlpatterns = [
    path('', include((router.urls, app_name), namespace="pgtc-api")),
    path('validation-processes/<str:course_id>/submit/', views.submit_validation_process, name="validation-process-submit"),
    path('validation-processes/<str:course_id>/update-state/', views.update_validation_process_state, name='validation-process-update-state'),
    path('validation-processes/<str:course_id>/', views.info_validation_process, name="validation-process-info"),
    path('validation-processes/', views.get_validation_processes, name="get-validation-processes"),
    path('user-info/', views.user_info, name="get_user_info"),
]
