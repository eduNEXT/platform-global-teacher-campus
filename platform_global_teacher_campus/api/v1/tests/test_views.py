from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase

from platform_global_teacher_campus.api.v1.tests import factories, utils


class TestValidationProcessFlow(APITestCase):

    def setUp(self) -> None:
        # Create a Validation Body with a validator
        self.validator = factories.UserFactory.create(
            username='validator'
        )
        self.validation_body = factories.ValidationBodyFactory.create(id=1, name="Test Body")
        self.validation_body.validators.add(self.validator)

        # Create a Course Author
        self.course_author = factories.UserFactory.create(
            username='course_author'
        )

        # Create a course
        self.course_id = "course-v1:edX+DemoX+Demo_Course"
        self.course = factories.CourseFactory.create(id=self.course_id)
        return super().setUp()

    @patch("platform_global_teacher_campus.models.CourseStaffRole")
    def test_create_validation_process(self, course_staff_role_mock):
        url = reverse(
            "pgtc-api:pgtc-api:validation-process-submit",
            kwargs={"course_id": self.course_id}
        )
        course_staff_role_mock.has_user.return_value = True
        data = {
            "category_ids": [
                1
            ],
            "validation_body_id": 1,
            "comment": "Test comment"
        }
        course_author_token = utils.create_jwt_token(self.course_author)
        print(course_author_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + course_author_token)
        breakpoint()
        response = self.client.post(url, data=data)
        print(response)
        assert True==True
