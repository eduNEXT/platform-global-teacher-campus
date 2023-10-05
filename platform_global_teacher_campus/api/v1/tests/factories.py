from django.contrib.auth import get_user_model
from factory import Factory, Faker
from factory.django import DjangoModelFactory

from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview
from platform_global_teacher_campus.models import ValidationBody

CourseOverview = get_course_overview()
User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

class CourseFactory(DjangoModelFactory):
    class Meta:
        model = CourseOverview

class OrganizationFactory(Factory):
    key = Faker('word')
    name = Faker('company')
    uuid = Faker('uuid4')
    logo_image_url = Faker('image_url')

class ValidationBodyFactory(DjangoModelFactory):
    """
    validators = models.ManyToManyField(User, related_name="validation_bodies")
    name = models.TextField()
    admin_notes = models.TextField(default="")
    organizations = models.ManyToManyField(Organization)
    """
    class Meta:
        model = ValidationBody
