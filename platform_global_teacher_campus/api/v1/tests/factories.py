from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from platform_global_teacher_campus.edxapp_wrapper.courses import get_course_overview

User = get_user_model()
CourseOverview = get_course_overview()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

class CourseFactory(DjangoModelFactory):
    class Meta:
        model = CourseOverview