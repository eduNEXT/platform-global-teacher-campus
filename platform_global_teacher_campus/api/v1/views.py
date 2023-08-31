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

    def is_valid_transition(self, current_status, new_status, allowed_transitions):
        return current_status in allowed_transitions.get(new_status, [])

    def validate_permissions(self, new_status, user, validation_process):
        user_allowed_status = {
            ValidationProcessEvent.StatusChoices.SUBMITTED: "user",
            ValidationProcessEvent.StatusChoices.IN_REVIEW: "validator",
            ValidationProcessEvent.StatusChoices.DRAFT: "validator",
            ValidationProcessEvent.StatusChoices.APPROVED: "validator",
            ValidationProcessEvent.StatusChoices.DISAPPROVED: "validator",
            ValidationProcessEvent.StatusChoices.CANCELLED: "user",
        }

        if user_allowed_status[new_status] == "user":
            if not self.has_publish_permissions(validation_process.course.id, user):
                error_msg = f"You don't have permissions on this course to do this action: {new_status}"
                return Response({"error": error_msg}, status=status.HTTP_403_FORBIDDEN)

        if user_allowed_status[new_status] == "validator":
            if not self.is_validator_of_validation_body(validation_process.validation_body, user):
                error_msg = f"You don't have permissions as validator to do this action: {new_status}"
                return Response({"error": error_msg}, status=status.HTTP_403_FORBIDDEN)

        return None

    def validate_transition(self, new_status, current_status, validation_process):
        allowed_transitions = {
            ValidationProcessEvent.StatusChoices.SUBMITTED: [
                None, ValidationProcessEvent.StatusChoices.DRAFT,
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

        transition_result = self.validate_transition(new_status, current_status, validation_process)
        if transition_result is not None:
            return transition_result

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

