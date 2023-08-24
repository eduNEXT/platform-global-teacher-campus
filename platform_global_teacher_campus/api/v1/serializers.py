from rest_framework import serializers
from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.edxapp_wrapper.users import get_user_model
from platform_global_teacher_campus.edxapp_wrapper.organizations import get_organization_model
from platform_global_teacher_campus.models import ValidationBody, CourseCategory

CourseOverview = get_course_overview()
User = get_user_model()
Organization = get_organization_model()


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id']


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ValidationBodySerializer(serializers.ModelSerializer):
    validators = UserEmailSerializer(many=True)
    organizations = OrganizationSerializer(many=True)

    class Meta:
        model = ValidationBody
        exclude = ['admin_notes']
