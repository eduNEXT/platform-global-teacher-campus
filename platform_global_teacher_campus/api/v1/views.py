"""
API v1 views.
"""

from platform_global_teacher_campus.models import (
    CourseCategory,
    ValidationBody,
    ValidationProcess,
    ValidationProcessEvent
)
from rest_framework import viewsets
from platform_global_teacher_campus.api.v1.serializers import (
    CourseCategorySerializer,
    ValidationBodySerializer,
    ValidationProcessSerializer,
    ValidationProcessEventSerializer
)


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class ValidationBodyViewSet(viewsets.ModelViewSet):
    queryset = ValidationBody.objects.all()
    serializer_class = ValidationBodySerializer


class ValidationProcessViewSet(viewsets.ModelViewSet):
    queryset = ValidationProcess.objects.all()
    serializer_class = ValidationProcessSerializer


class ValidationProcessEventViewSet(viewsets.ModelViewSet):
    queryset = ValidationProcessEvent.objects.all()
    serializer_class = ValidationProcessEventSerializer
