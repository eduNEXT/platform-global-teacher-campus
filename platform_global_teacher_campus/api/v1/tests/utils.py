"""
Utils for tests authentication.
"""

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def create_jwt_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
