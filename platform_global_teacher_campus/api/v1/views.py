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


def user_has_publish_permissions(course_key, user):
    return CourseStaffRole(course_key).has_user(user)


def is_validator_of_validation_body(validation_body, user):
    return user in validation_body.validators.all()


def is_valid_transition(current_status, new_status, allowed_transitions):
    return current_status in allowed_transitions.get(new_status, [])


def validate_permissions(new_status, user, validation_process):
    user_allowed_status = {
        ValidationProcessEvent.StatusChoices.SUBMITTED: "both",
        ValidationProcessEvent.StatusChoices.IN_REVIEW: "validator",
        ValidationProcessEvent.StatusChoices.DRAFT: "validator",
        ValidationProcessEvent.StatusChoices.APPROVED: "validator",
        ValidationProcessEvent.StatusChoices.DISAPPROVED: "validator",
        ValidationProcessEvent.StatusChoices.CANCELLED: "user",
    }

    if user_allowed_status[new_status] in ["user", "both"]:
        if not user_has_publish_permissions(validation_process.course.id, user):
            error_msg = f"You don't have permissions on this course to do this action: {new_status}"
            return Response({"detail": error_msg}, status=status.HTTP_403_FORBIDDEN)

    if user_allowed_status[new_status] in ["validator", "both"]:
        print("ESTE ES VALIDADOR? NO SABIA", is_validator_of_validation_body(validation_process.validation_body, user))
        if not is_validator_of_validation_body(validation_process.validation_body, user):
            error_msg = f"You don't have permissions as validator to do this action: {new_status}"
            return Response({"detail": error_msg}, status=status.HTTP_403_FORBIDDEN)

    return None


def validate_transition(new_status, current_status):
    allowed_transitions = {
        ValidationProcessEvent.StatusChoices.SUBMITTED: [
            None,
            ValidationProcessEvent.StatusChoices.DRAFT,
            # This allows one validator to release a course for review by another validator.
            ValidationProcessEvent.StatusChoices.IN_REVIEW,
            ValidationProcessEvent.StatusChoices.CANCELLED,
        ],
        ValidationProcessEvent.StatusChoices.IN_REVIEW: [
            ValidationProcessEvent.StatusChoices.DRAFT, ValidationProcessEvent.StatusChoices.SUBMITTED,
        ],
        ValidationProcessEvent.StatusChoices.DRAFT: [
            ValidationProcessEvent.StatusChoices.IN_REVIEW,
        ],
        ValidationProcessEvent.StatusChoices.APPROVED: [
            ValidationProcessEvent.StatusChoices.IN_REVIEW,
        ],
        ValidationProcessEvent.StatusChoices.DISAPPROVED: [
            ValidationProcessEvent.StatusChoices.IN_REVIEW,
        ],
        ValidationProcessEvent.StatusChoices.CANCELLED: [
            ValidationProcessEvent.StatusChoices.DRAFT, ValidationProcessEvent.StatusChoices.SUBMITTED,
        ],
    }

    if not is_valid_transition(current_status, new_status, allowed_transitions):
        error_msg = f"This action ({new_status}) can't be applied because the previous action is {current_status}"
        return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)
    return None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def submit_validation_process(request, course_id):
    course_id = CourseOverview.objects.get(id=course_id).id

    if ValidationProcess.get_from_course_id(course_id):
        return Response({"detail": "There is already a validation process for this course."}, status=status.HTTP_409_CONFLICT)

    if not user_has_publish_permissions(course_id, request.user):
        return Response({"detail": "The user doesn't have permissions to do this action."}, status=status.HTTP_401_UNAUTHORIZED)

    data = {
        "course_id": str(course_id),
        "category_ids": request.data.get("categories"),
        "validation_body_id": request.data.get("validation_body"),
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

        permissions_result = validate_permissions(new_status, request.user, validation_process)
        if permissions_result is not None:
            return permissions_result

        transition_result = validate_transition(new_status, current_status)
        if transition_result is not None:
            return transition_result

        serializer.save(validation_process=validation_process)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
