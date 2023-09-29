#!/usr/bin/env python
"""
Tests for the `platform-global-teacher-campus` models module.
"""

from unittest.mock import patch
import requests
from rest_framework import status
from platform_global_teacher_campus.api.v1.views import create_validation_process_event


@patch('platform_global_teacher_campus.api.v1.views.create_validation_process_event')
def test_update_validation_process_state_with_requests(mock_create):
    # Define your test data and request payload

    jwt_token = "your-token"

    payload = {
        "status": "revi",
        "comment": "Test comment",
        # Add any other required fields in the payload
    }

    invalid_payload_missing_status = {
        "comment": "Test comment",

    }

    invalid_payload_missing_comment = {
        "status": "revi",

    }

    # Construct the URL for your endpoint
    url = "your-domain/plugin-cvw/api/v1/validation-processes/your-course/update-state/"

    session = requests.Session()

    session.headers.update({'Authorization': f'jwt {jwt_token}'})

    response = session.post(url, json=payload)

    response_invalid_missing_status = session.post(url, json=invalid_payload_missing_status)

    response_invalid_missing_comment = session.post(url, json=invalid_payload_missing_comment)

    assert response.status_code == status.HTTP_201_CREATED
    assert response_invalid_missing_status.status_code == 400
    assert response_invalid_missing_comment.status_code == 400

    response_data = response.json()
    assert response_data['status'] == 'revi'
    assert response_data['comment'] == 'Test comment'
