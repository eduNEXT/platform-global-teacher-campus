""" urls.py """

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from platform_global_teacher_campus.api.v1 import views

app_name = 'platform_global_teacher_campus'

router = DefaultRouter()
router.register(r'categories', views.CourseCategoryViewSet)
router.register(r'validation-bodies', views.ValidationBodyViewSet)

urlpatterns = [

    path(
        'validation-processes/<str:course_id>/submit/',
        views.submit_validation_process,
        name="validation-process-submit"),
    path(
        'validation-processes/<str:course_id>/update-state/',
        views.update_validation_process_state,
        name='validation-process-update-state'),
    path('validation-processes/<str:course_id>/', views.info_validation_process, name="validation-process-info"),
    path('validation-processes/', views.get_validation_processes, name="get-validation-processes"),
    path('user-info/', views.user_info, name="get_user_info"),
    path('rejection-reasons/', views.get_rejection_reasons, name="get-rejection-reasons"),
    path('validation-bodies/<str:course_id>/',
         views.get_validation_bodies_by_course,
         name="get-validation-bodies-by-course"),
    path('', include((router.urls, app_name), namespace="pgtc-api")),

]
