"""
API v1 views.
"""

from platform_global_teacher_campus.models import CourseCategory
from rest_framework import viewsets
from platform_global_teacher_campus.api.v1.serializers import CourseCategorySerializer

class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
