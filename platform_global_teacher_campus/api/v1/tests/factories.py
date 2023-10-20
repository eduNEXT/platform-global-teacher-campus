"""
factories of mocked data for tests
"""

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory
from organizations.models import Organization

from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.models import (
    ValidationBody,
    ValidationProcess,
    ValidationProcessEvent,
    ValidationRules,
)

CourseOverview = get_course_overview()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    """
    factory for the user model
    """
    class Meta:
        model = User


class CourseFactory(DjangoModelFactory):
    """
    factory for the course model
    """
    class Meta:
        model = CourseOverview

    org = Faker('company')
    display_name = Faker('word')


class OrganizationFactory(DjangoModelFactory):
    """
    factory for the organization model
    """
    class Meta:
        model = Organization


class ValidationBodyFactory(DjangoModelFactory):
    """
    factory for the uvalidation body model
    """
    class Meta:
        model = ValidationBody


class ValidationProcessFactory(DjangoModelFactory):
    """
    factory for the validation process model
    """
    class Meta:
        model = ValidationProcess


class ValidationProcessEventFactory(DjangoModelFactory):
    """
    factory for the validation process event model
    """
    class Meta:
        model = ValidationProcessEvent


class ValidationRulesFactory(DjangoModelFactory):
    """
    factory for the validation rules model
    """
    class Meta:
        model = ValidationRules
