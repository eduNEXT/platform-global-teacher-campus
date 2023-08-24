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
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField()
    short_name = serializers.ReadOnlyField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'short_name']


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ValidationBodySerializer(serializers.ModelSerializer):
    validators = UserEmailSerializer(many=True, read_only=False)
    organizations = OrganizationSerializer(many=True, read_only=False)

    class Meta:
        model = ValidationBody
        exclude = ['admin_notes']

    def create(self, validated_data):
        validators_data = validated_data.pop('validators')
        organizations_data = validated_data.pop('organizations')

        validation_body = ValidationBody.objects.create(**validated_data)

        for validator_data in validators_data:
            email = validator_data['email']
            try:
                user = User.objects.get(email=email)
                validation_body.validators.add(user)
            except User.DoesNotExist:
                pass

            for org_data in organizations_data:
                org_id = org_data["id"]
                try:
                    organization = Organization.objects.get(id=org_id)
                    validation_body.organizations.add(organization)
                except Organization.DoesNotExist:
                    pass

            return validation_body
