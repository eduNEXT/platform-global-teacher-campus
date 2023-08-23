""" urls.py """

from django.urls import path
from . import views

app_name = 'platform_global_teacher_campus'

urlpatterns = [
    path('', views.index, name='index'),
    path('validation/<int:process_id>/', views.validation_process_detail, name='validation_process_detail'),
]
