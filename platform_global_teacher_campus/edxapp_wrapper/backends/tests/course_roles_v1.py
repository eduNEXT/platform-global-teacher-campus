"""
Backend about Course Roles.
"""
from unittest.mock import MagicMock


def get_course_staff_role():
    return MagicMock


def get_course_access_role():
    mock_role = MagicMock()
    mock_objects = MagicMock()

    # Mock queryset-like object
    mock_queryset = MagicMock()

    # Assign the delete method to the mock queryset
    mock_queryset.delete = MagicMock()

    # Set the filter to return the queryset mock
    mock_objects.filter.return_value = mock_queryset

    mock_role.objects = mock_objects
    return mock_role


def get_global_staff():
    return MagicMock
