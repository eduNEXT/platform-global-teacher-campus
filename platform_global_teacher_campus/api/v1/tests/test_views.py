"""
Tests for the happy path for a course validation.
"""

import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from platform_global_teacher_campus.api.v1.tests import factories, utils


class TestValidationProcessFlow(APITestCase):
    """
    Class for testing the basic validation process for a course.
    """

    def setUp(self) -> None:
        # Create a Validation Body with a validator
        self.validator = factories.UserFactory.create(
            username='validator'
        )
        self.validation_body = factories.ValidationBodyFactory.create(id=1, name="Test Body")
        self.validation_body.validators.add(self.validator)

        self.validation_body_excempt = factories.ValidationBodyFactory.create(id=2, name="Excempt Body")
        self.validation_body_excempt.validators.add(self.validator)

        self.organization = factories.OrganizationFactory.create(name='company', short_name='comp')

        self.organization_exempt = factories.OrganizationFactory.create(name='company_exempt', short_name='compex')

        # Create a Course Author
        self.course_author = factories.UserFactory.create(
            username='course_author'
        )

        # Create a course
        self.course_id = 'course-v1:edX+DemoX+Demo_Course'
        self.course_id_exempt = 'course-v1:edX+ExemptX+Exempt_Course'

        self.course = factories.CourseFactory.create(
            id=self.course_id,
            org='comp'
        )
        self.course_exempt = factories.CourseFactory.create(
            id=self.course_id_exempt,
            org='compex'
        )

        self.validation_rule = factories.ValidationRulesFactory.create(
            permission_type="vb_exempt",
            validation_body=self.validation_body_excempt,
            organization=self.organization_exempt,
            is_active=True
        )

        self.client = APIClient()

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
        data_json = json.dumps(data)
        course_author_token = utils.create_jwt_token(self.course_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + course_author_token)
        # breakpoint()
        response = self.client.post(url, data=data_json, content_type='application/json')

        assert response.status_code == 201

    @patch('platform_global_teacher_campus.api.v1.views.publish_course')
    @patch("platform_global_teacher_campus.models.CourseStaffRole")
    def test_update_validation_process_state(self, course_staff_role_mock, mock_publish_course):
        course_staff_role_mock.has_user.return_value = True
        mock_publish_course.return_value = None

        # Given: A ValidationProcess exists for the course
        validation_process = factories.ValidationProcessFactory.create(
            course=self.course,
            organization=self.organization,
            current_validation_user=self.validator,
            validation_body=self.validation_body,
        )
        validation_process_event = factories.ValidationProcessEventFactory.create(  # pylint: disable=unused-variable
            validation_process=validation_process,
        )

        url = reverse(
            "pgtc-api:pgtc-api:validation-process-update-state",
            kwargs={"course_id": self.course.id}
        )
        validator_token = utils.create_jwt_token(self.validator)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + validator_token)
        data = {
            "status": "revi",  # Or any other status you'd like to test
            "comment": "review comment"
        }
        data_approved = {
            "status": "aprv",  # Or any other status you'd like to test
            "comment": "approved comment"
        }
        response = self.client.post(url, data=data, format='json')

        assert response.status_code == 201

        response_approved = self.client.post(url, data=data_approved, format='json')

        mock_publish_course.assert_called_once()
        assert response_approved.status_code == 201

    @patch('platform_global_teacher_campus.api.v1.serializers.publish_course')
    @patch("platform_global_teacher_campus.models.CourseStaffRole")
    def test_validation_rules(self, course_staff_role_mock, mock_publish_course):
        course_staff_role_mock.has_user.return_value = True
        mock_publish_course.return_value = None
        url = reverse(
            "pgtc-api:pgtc-api:validation-process-submit",
            kwargs={"course_id": self.course_id_exempt}
        )

        data = {
            "category_ids": [
                1
            ],
            "validation_body_id": 2,
            "comment": "Exempt comment"
        }
        data_json = json.dumps(data)
        course_author_token = utils.create_jwt_token(self.course_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + course_author_token)
        # breakpoint()
        response = self.client.post(url, data=data_json, content_type='application/json')

        assert response.status_code == 201

        # Extract events
        events = response.data.get('events', [])

        # Extract the desired event
        desired_event = next((event for event in events if event.get('comment') ==
                             'this course was automatic published due to exempt rules.'), None)

        # Assertions
        assert desired_event is not None, "Desired event not found in response"
        assert desired_event.get('status') == 'exmp'
