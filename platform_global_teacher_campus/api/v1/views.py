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
from rest_framework.permissions import IsAuthenticated
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class ValidationBodyViewSet(viewsets.ModelViewSet):
    queryset = ValidationBody.objects.all()
    serializer_class = ValidationBodySerializer


class ValidationProcessViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JwtAuthentication,)
    queryset = ValidationProcess.objects.all()
    serializer_class = ValidationProcessSerializer


class ValidationProcessEventViewSet(viewsets.ModelViewSet):
    queryset = ValidationProcessEvent.objects.all()
    serializer_class = ValidationProcessEventSerializer
