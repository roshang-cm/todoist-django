from django.http import JsonResponse
from todoist.settings import SECRET_KEY
import jwt


def resolve_user_id_from_jwt(request):
    PREFIX = 'Bearer '
    jwt_header = request.headers.get('authorization', '')
    if not jwt_header.startswith(PREFIX):
        raise PermissionError('JWT is not present')
    jwt_token = jwt_header[len(PREFIX):]
    return jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256']).get('id')


def get_jwt_for_id(id):
    return jwt.encode({'id': id}, SECRET_KEY, algorithm='HS256').decode("utf-8")


class StandardResponse(JsonResponse):

    def __init__(self, data=None, errors=None, status=200):
        render_data = {
            'data': data,
            'errors': errors
        }
        if (not data and errors) and status == 200:
            status = 400

        super().__init__(render_data, status=status)
