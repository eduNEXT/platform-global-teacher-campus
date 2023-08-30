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
from rest_framework.response import Response
from rest_framework import status
from platform_global_teacher_campus.api.v1.serializers import (
    CourseCategorySerializer,
    ValidationBodySerializer,
    ValidationProcessSerializer,
    ValidationProcessEventSerializer
)
from platform_global_teacher_campus.edxapp_wrapper.users import get_user_model
from platform_global_teacher_campus.edxapp_wrapper.course_roles import get_course_staff_role

User = get_user_model()
CourseStaffRole = get_course_staff_role()

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


    def has_publish_permissions(self, course_key, user):
        return CourseStaffRole(course_key).has_user(user)

    def is_validator_of_validation_body(self, validation_body, user):
        return user in validation_body.validators.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validation_process = serializer.validated_data['validation_process']
        # user = self.request.user  # El usuario que está haciendo la solicitud  
        user = User.objects.get(id=4) # ToDo
        
        # Verificar si el usuario es course authoring y tiene permisos de publicar
        has_publish_permissions = self.has_publish_permissions(validation_process.course.id, user)

        # Obtener el estado anterior del último ValidationProcessEvent
        previous_event = validation_process.events.last()
        previous_status = previous_event.status if previous_event else None

        
        if serializer.validated_data['status'] == 'subm':
            if not has_publish_permissions or previous_status not in ['drft', None]:
                return Response({"error": "No tienes permiso para enviar 'subm'"}, status=status.HTTP_403_FORBIDDEN)
        
        elif serializer.validated_data['status'] == 'revi':
            # Verificar si el usuario es un validator del validation body y el estado anterior es drft o subm
            if not self.is_validator_of_validation_body(validation_process.validation_body, user) or previous_status not in ['drft', 'subm']:
                return Response({"error": "No tienes permiso para enviar 'revi'"}, status=status.HTTP_403_FORBIDDEN)
        
        elif serializer.validated_data['status'] == 'drft':
            # Verificar si el usuario es un validator del validation body y el estado anterior es in_review
            if not self.is_validator_of_validation_body(validation_process.validation_body, user) or previous_status != 'in_review':
                return Response({"error": "No tienes permiso para enviar 'drft'"}, status=status.HTTP_403_FORBIDDEN)
        
        elif serializer.validated_data['status'] in ['aprv', 'dprv']:
            # Verificar si el usuario es un validator del validation body y el estado anterior es in_review
            if not self.is_validator_of_validation_body(validation_process.validation_body, user) or previous_status != 'in_review':
                return Response({"error": "No tienes permiso para enviar 'aprv' o 'dprv'"}, status=status.HTTP_403_FORBIDDEN)
        
        elif serializer.validated_data['status'] == 'cncl':
            if not has_publish_permissions or previous_status not in ['drft', 'subm']:
                return Response({"error": "No tienes permiso para enviar 'cncl'"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
