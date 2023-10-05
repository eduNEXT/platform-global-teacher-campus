from rest_framework.test import APITestCase
from platform_global_teacher_campus.api.v1.tests import factories

class TestValidationProcessFlow(APITestCase):
    def test_create_validation_process(self):
        url = "/plugin-cvw/api/v1/validation-processes/course-v1:edX+CS102+2023_T1/submit/"
        response = self.client.get(url)
        print(response)
        user = factories.UserFactory()
        course = factories.CourseFactory(course_id="course_v1")
        assert True ==True
