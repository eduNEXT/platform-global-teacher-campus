from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse



class UpdateValidationProcessStateTestCase(TestCase):

    def setUp(self):
        """ setup """
        super().setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)

    def test_update_validation_process_state(self):
        
        course_id = 'course-v1:edX+CS102+2023_T1'
        payload = {
            "status": "revi",
            "comment": "Test comment",
        }
        
        url = reverse('api/v1/validation-processes/course-v1:edX+CS102+2023_T1/update-state/', args=[course_id])
        
        # Send a POST request to the endpoint
        response = self.client.post(url, data=payload, format='json')
        
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(response.data['status'], 'revi')
        self.assertEqual(response.data['comment'], 'Test comment')








