"""
Module for serializers.
"""
from django.contrib.auth import get_user_model
from organizations.models import Organization
from rest_framework import serializers

from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.models import (
    CourseCategory,
    ValidationBody,
    ValidationProcess,
    ValidationProcessEvent,
    ValidationRejectionReason,
    ValidationRules,
)

from .publish_utils import publish_course

CourseOverview = get_course_overview()
User = get_user_model()


class CourseCategorySerializer(serializers.ModelSerializer):
    """
    The serializer for the CourseCategory model.
    """
    class Meta:
        model = CourseCategory
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    """
    The serializer for the Organization model.
    """
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField()
    short_name = serializers.ReadOnlyField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_name']


class UserSerializer(serializers.ModelSerializer):
    """
    The serializer for the User model.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else None


class ValidationBodySerializer(serializers.ModelSerializer):
    """
    The serializer for the ValidationBody model.
    """
    validators = UserSerializer(many=True, read_only=True)
    organizations = OrganizationSerializer(many=True, read_only=True)

    validator_emails = serializers.ListField(child=serializers.CharField(), write_only=True)
    organization_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = ValidationBody
        exclude = ['admin_notes']

    def create(self, validated_data):
        validator_emails = validated_data.pop('validator_emails')
        organization_ids = validated_data.pop('organization_ids')

        validation_body = ValidationBody.objects.create(**validated_data)

        for email in validator_emails:
            try:
                user = User.objects.get(email=email)
                validation_body.validators.add(user)
            except User.DoesNotExist:
                pass

        for org_id in organization_ids:
            try:
                organization = Organization.objects.get(id=org_id)
                validation_body.organizations.add(organization)
            except Organization.DoesNotExist:
                pass

        return validation_body


class CourseSerializer(serializers.ModelSerializer):
    """
    The serializer for the CourseOverview model.
    """
    class Meta:
        model = CourseOverview
        fields = ["id", "display_name"]


class ValidationRejectionReasonSerializer(serializers.ModelSerializer):
    """
    The serializer for the ValidationRejectionReason model.
    """
    class Meta:
        model = ValidationRejectionReason
        fields = "__all__"


class ValidationProcessEventSerializer(serializers.ModelSerializer):
    """
    The serializer for the ValidationProcessEvent model.
    """
    user = UserSerializer(read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = ValidationProcessEvent
        fields = "__all__"

    def get_username(self, obj):
        # Retrieve the username of the user associated with the event
        return obj.user.username if obj.user else None


class ValidationProcessSerializer(serializers.ModelSerializer):
    """
    The serializer for the ValidationProcess model.
    """
    course = CourseSerializer(read_only=True)
    categories = CourseCategorySerializer(many=True, read_only=True)
    organization = OrganizationSerializer(read_only=True)
    current_validation_user = UserSerializer(read_only=True)
    validation_body = ValidationBodySerializer(read_only=True)
    events = ValidationProcessEventSerializer(many=True, read_only=True)

    course_id = serializers.CharField(write_only=True)
    validation_body_id = serializers.IntegerField(write_only=True)
    category_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    comment = serializers.CharField(write_only=True)

    class Meta:
        model = ValidationProcess
        fields = "__all__"

    def apply_validation_rules(self, validation_process, user) -> any:
        is_org_exempt = ValidationRules.objects.filter(
            is_active=True,
            organization=validation_process.organization,
            permission_type=ValidationRules.PermissionTypeChoices.ORG_EXEMPT
        ).exists()

        is_user_exempt = ValidationRules.objects.filter(
            is_active=True,
            organization=validation_process.organization,
            user=user,
            permission_type=ValidationRules.PermissionTypeChoices.USER_EXEMPT
        ).exists()

        is_vd_exempt = ValidationRules.objects.filter(
            is_active=True,
            organization=validation_process.organization,
            validation_body=validation_process.validation_body,
            permission_type=ValidationRules.PermissionTypeChoices.VALIDATION_BODY_EXEMPT
        ).exists()

        if is_org_exempt or is_user_exempt or is_vd_exempt:
            data = {
                'comment': 'this course was automatic published due to exempt rules.',
                'status': ValidationProcessEvent.StatusChoices.EXEMPT,
                'validation_process': validation_process,
                'user': user
            }
            self.create_event(data=data)

            # Publish course
            publish_result = publish_course(validation_process.course, user)
            print(publish_result)

    def create_event(self, data) -> None:
        ValidationProcessEvent.objects.create(
            validation_process=data.get("validation_process"),
            status=data.get("status"),
            comment=data.get("comment"),
            user=data.get("user")
        )

    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        category_ids = validated_data.pop('category_ids')
        validation_body_id = validated_data.pop('validation_body_id')
        submitted_comment = validated_data.pop('comment', None)

        try:
            course = CourseOverview.objects.get(id=course_id)
            organization = Organization.objects.get(short_name=course.org)
        except CourseOverview.DoesNotExist:
            course = None
            organization = None

        try:
            validation_body = ValidationBody.objects.get(id=validation_body_id)
        except ValidationBody.DoesNotExist:
            validation_body = None

        validation_process = ValidationProcess.objects.create(
            course=course,
            organization=organization,
            validation_body=validation_body,
            **validated_data
        )
        categories = CourseCategory.objects.filter(id__in=category_ids)
        validation_process.categories.add(*categories)

        self.create_event(data={
            'status': ValidationProcessEvent.StatusChoices.SUBMITTED,
            'validation_process': validation_process,
            'comment': submitted_comment,
            'user': self.context['request'].user,
        })

        self.apply_validation_rules(validation_process, self.context['request'].user)

        return validation_process
