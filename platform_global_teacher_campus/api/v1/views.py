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


class ValidationProcessEventViewSet(viewsets.ModelViewSet):
    queryset = ValidationProcessEvent.objects.all()
    serializer_class = ValidationProcessEventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JwtAuthentication,)

    def has_publish_permissions(self, course_key, user):
        return CourseStaffRole(course_key).has_user(user)

    def is_validator_of_validation_body(self, validation_body, user):
        return user in validation_body.validators.all()

    def is_valid_transition(self, current_status, new_status, allowed_transitions):
        return current_status in allowed_transitions.get(new_status, [])

    def validate_permissions(self, new_status, user, validation_process):
        user_allowed_status = {
            ValidationProcessEvent.StatusChoices.SUBMITTED: "both",
            ValidationProcessEvent.StatusChoices.IN_REVIEW: "validator",
            ValidationProcessEvent.StatusChoices.DRAFT: "validator",
            ValidationProcessEvent.StatusChoices.APPROVED: "validator",
            ValidationProcessEvent.StatusChoices.DISAPPROVED: "validator",
            ValidationProcessEvent.StatusChoices.CANCELLED: "user",
        }

        if user_allowed_status[new_status] in ["user", "both"]:
            if not self.has_publish_permissions(validation_process.course.id, user):
                error_msg = f"You don't have permissions on this course to do this action: {new_status}"
                return Response({"error": error_msg}, status=status.HTTP_403_FORBIDDEN)

        if user_allowed_status[new_status] in ["validator", "both"]:
            if not self.is_validator_of_validation_body(validation_process.validation_body, user):
                error_msg = f"You don't have permissions as validator to do this action: {new_status}"
                return Response({"error": error_msg}, status=status.HTTP_403_FORBIDDEN)

        return None

    def validate_transition(self, new_status, current_status):
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

        if not self.is_valid_transition(current_status, new_status, allowed_transitions):
            error_msg = f"This action ({new_status}) can't be applied because the previous action is {current_status}"
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        validation_process = serializer.validated_data['validation_process']
        current_event = validation_process.events.last()
        current_status = current_event.status if current_event else None
        new_status = serializer.validated_data['status']

        permissions_result = self.validate_permissions(new_status, user, validation_process)
        if permissions_result is not None:
            return permissions_result

        transition_result = self.validate_transition(new_status, current_status)
        if transition_result is not None:
            return transition_result

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def user_has_publish_permissions(course_key, user):
    return CourseStaffRole(course_key).has_user(user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def submit_validation_process(request, course_id):
    course_id = CourseOverview.objects.get(id=course_id).id

    if ValidationProcess.get_from_course_id(course_id):
        detail = {
            "detail": "There is already a validation process for this course."
        }
        return Response(detail, status=status.HTTP_409_CONFLICT)

    if not user_has_publish_permissions(course_id, request.user):
        detail = {
            "detail": "The user doesn't have permissions to do this action."
        }
        return Response(detail, status=status.HTTP_401_UNAUTHORIZED)

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
