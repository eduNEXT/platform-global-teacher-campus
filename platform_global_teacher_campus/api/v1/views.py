"""
API v1 views.
"""
from django.contrib.auth import get_user_model
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from platform_global_teacher_campus.api.v1.serializers import (
    CourseCategorySerializer,
    ValidationBodySerializer,
    ValidationProcessEventSerializer,
    ValidationProcessSerializer,
    ValidationRejectionReasonSerializer,
)
from platform_global_teacher_campus.edxapp_wrapper.course_roles import (
    get_course_access_role,
    get_course_staff_role,
    get_global_staff,
)
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.models import (
    CourseCategory,
    Organization,
    ValidationBody,
    ValidationProcess,
    ValidationProcessEvent,
    ValidationRejectionReason,
)

from .publish_utils import publish_course

User = get_user_model()
CourseStaffRole = get_course_staff_role()
CourseOverview = get_course_overview()
GlobalStaff = get_global_staff()
CourseAccessRole = get_course_access_role()


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    pagination_class = None  # This disables pagination
    http_method_names = ['get']  # Only allow GET requests


class ValidationBodyViewSet(viewsets.ModelViewSet):
    queryset = ValidationBody.objects.all()
    serializer_class = ValidationBodySerializer
    pagination_class = None  # This disables pagination
    http_method_names = ['get']  # Only allow GET requests


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
        return Response({"detail": "There is already a validation process for this course."},
                        status=status.HTTP_409_CONFLICT)

    if not ValidationProcess.can_user_submit(request.user, course_id):
        return Response({"detail": "The user doesn't have permissions to do this action."},
                        status=status.HTTP_401_UNAUTHORIZED)

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
        return Response({"detail": "There is not a validation process for this course_id."},
                        status=status.HTTP_404_NOT_FOUND)

    if not request.data.get("status") or not request.data.get("comment"):
        return Response({"details": "Remember to specify the status and comment in the request."},
                        status=status.HTTP_400_BAD_REQUEST)

    validator_course_access_role = CourseAccessRole.objects.filter(
        user=request.user, course_id=course_id, org=validation_process.organization.name)
    new_status = request.data.get("status")

    if not ValidationProcessEvent.can_user_update_to(request.user, validation_process, new_status):
        return Response({"detail": "The user doesn't have permissions to do this action."},
                        status=status.HTTP_401_UNAUTHORIZED)

    if not ValidationProcessEvent.can_transition_from_to(current_status, new_status):
        error_msg = f"This action ({new_status}) can't be applied because the previous action is {current_status}"
        return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)

    if new_status == ValidationProcessEvent.StatusChoices.IN_REVIEW:
        validation_process.current_validation_user = request.user
        validation_process.save()

    if new_status == ValidationProcessEvent.StatusChoices.SUBMITTED and validation_process.validation_body.is_validator(
            request.user):
        validation_process.current_validation_user = None
        validator_course_access_role.delete()
        validation_process.save()

    if new_status == ValidationProcessEvent.StatusChoices.APPROVED:
        publish_course(validation_process.course, request.user)

    if new_status in [ValidationProcessEvent.StatusChoices.DRAFT, ValidationProcessEvent.StatusChoices.DISAPPROVED,
                      ValidationProcessEvent.StatusChoices.APPROVED]:
        validator_course_access_role.delete()

    process_event = ValidationProcessEvent.objects.create(
        validation_process=validation_process,
        status=new_status,
        comment=request.data.get("comment"),
        user=request.user,
        reason_id=request.data.get("reason")
    )

    return Response(ValidationProcessEventSerializer(process_event).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def info_validation_process(request, course_id):
    try:
        validation_process = ValidationProcess.objects.get(course_id=course_id)
        serializer = ValidationProcessSerializer(validation_process)  # Serialize the ValidationProcess object
        return Response(serializer.data)  # Return serialized data as JSON
    except ValidationProcess.DoesNotExist:
        return Response({"error": "Validation process not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def get_validation_processes(request):
    """
    Returns the validation processes visible for the username provided or the request user.

    **Example Requests**

    GET /plugin-cvw/api/v1/validation-processes/?username=validator-1

    GET /plugin-cvw/api/v1/validation-processes/

    **Params**

    - `username` (optional, string, _query_params_) - defaults to the calling user if not provided.

    **Responses**

    - 200: Success.

    - 404: Not found.
    """

    try:
        username = request.query_params.get('username') or request.user.username
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Only staff members can view validation processes from other users.
    # We don't use 401 to not let them deduce the existence of an user.
    if user != request.user and not GlobalStaff().has_user(request.user):
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check the validation processes of the courses to which a user has access due to their role in the courses.
    course_access_roles = list(CourseAccessRole.objects.filter(user=user).exclude(course_id=None))
    course_accesses = [course_access.course_id for course_access in course_access_roles]
    query_course_access = ValidationProcess.objects.filter(course__in=course_accesses)

    # Check the validation processes by their Validation Bodies
    validation_bodies = list(ValidationBody.objects.filter(validators=user))
    query_validation_body = ValidationProcess.objects.filter(validation_body__in=validation_bodies)

    validation_processes_allowed = list(query_course_access.union(query_validation_body).all())
    serialized_validation_processes_allowed = [
        ValidationProcessSerializer(validation_process).data for
        validation_process in validation_processes_allowed
    ]

    return Response(
        status=status.HTTP_200_OK,
        data=serialized_validation_processes_allowed
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def user_info(request):
    """
    Return extra info of the authenticated user.

    **Example Requests**

    GET /plugin-cvw/api/v1/user-info/

    **Responses**

    - 200: Success.
    """
    response = {
        "is_validator": request.user.validation_bodies.count() > 0
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def get_rejection_reasons(request):
    rejection_reasons = ValidationRejectionReason.objects.all()

    if not rejection_reasons:  # Check if the queryset is empty
        return Response(data={}, status=status.HTTP_200_OK)

    serializer = ValidationRejectionReasonSerializer(rejection_reasons, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JwtAuthentication])
def get_validation_bodies_by_course(request, course_id):
    try:
        course = CourseOverview.objects.get(id=course_id)
    except CourseOverview.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    organization_of_course = course.org
    organization_id = Organization.objects.get(name=organization_of_course).id
    validation_bodies_by_org = ValidationBody.objects.filter(organizations=organization_id)
    serializer = ValidationBodySerializer(validation_bodies_by_org, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
