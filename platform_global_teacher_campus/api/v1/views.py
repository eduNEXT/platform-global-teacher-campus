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
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from rest_framework.permissions import IsAuthenticated
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

User = get_user_model()
CourseStaffRole = get_course_staff_role()
CourseOverview = get_course_overview()


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def submit_validation_process(request, course_id):
    course_id = CourseOverview.objects.get(id=course_id).id

    if ValidationProcess.get_from_course_id(course_id):
        return Response({"detail": "There is already a validation process for this course."}, status=status.HTTP_409_CONFLICT)

    if not ValidationProcess.can_user_submit(request.user, course_id):
        return Response({"detail": "The user doesn't have permissions to do this action."}, status=status.HTTP_401_UNAUTHORIZED)

    data = {
        "course_id": str(course_id),
        "category_ids": request.data.get("category_ids"),
        "validation_body_id": request.data.get("validation_body_id"),
        "comment": request.data.get("comment"),
    }

    serializer = ValidationProcessSerializer(data=data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def update_validation_process_state(request, course_id):
    course_id = CourseOverview.objects.get(id=course_id).id
    try:
        validation_process = ValidationProcess.objects.get(course_id=course_id)
        current_event = validation_process.events.last()
        current_status = current_event.status if current_event else None
    except ValidationProcess.DoesNotExist:
        return Response({"detail": "There is not a validation process for this course_id."}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "validation_process": validation_process.id,
        "status": request.data.get("status"),
        "comment": request.data.get("comment"),
        "reason": request.data.get("reason"),
    }

    serializer = ValidationProcessEventSerializer(data=data)
    if serializer.is_valid():
        new_status = serializer.validated_data["status"]

        if not ValidationProcessEvent.can_user_update_to(request.user, validation_process, new_status):
            return Response({"detail": "The user doesn't have permissions to do this action."}, status=status.HTTP_401_UNAUTHORIZED)

        if not ValidationProcessEvent.can_transition_from_to(current_status, new_status):
            error_msg = f"This action ({new_status}) can't be applied because the previous action is {current_status}"
            return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(validation_process=validation_process)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
