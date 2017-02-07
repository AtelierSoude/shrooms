from users.serializers import UserShortSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    "Overrides DRF JWT to send back user infos along with JWT"
    return {
        'token': token,
        'user': UserShortSerializer(user, context={'request': request}).data
    }
