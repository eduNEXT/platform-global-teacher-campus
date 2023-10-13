from django.contrib.auth import get_user_model
from factory import Factory, Faker
from factory.django import DjangoModelFactory

from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.models import ValidationBody, ValidationProcess, ValidationProcessEvent, ValidationRules
from platform_global_teacher_campus.edxapp_wrapper.backends.tests.courses_v1 import CourseOverviewTestModel
from organizations.models import Organization

CourseOverview = get_course_overview()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = CourseOverview

    org = Faker('company')
    display_name = Faker('word')


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization


class ValidationBodyFactory(DjangoModelFactory):
    """
    validators = models.ManyToManyField(User, related_name="validation_bodies")
    name = models.TextField()
    admin_notes = models.TextField(default="")
    organizations = models.ManyToManyField(Organization)
    """
    class Meta:
        model = ValidationBody


class ValidationProcessFactory(DjangoModelFactory):
    class Meta:
        model = ValidationProcess


class ValidationProcessEventFactory(DjangoModelFactory):
    class Meta:
        model = ValidationProcessEvent


class ValidationRulesFactory(DjangoModelFactory):
    class Meta:
        model = ValidationRules
