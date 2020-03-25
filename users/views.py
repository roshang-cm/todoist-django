from django.contrib.auth.hashers import check_password
from todoist.response import StandardResponse, get_jwt_for_id
from users.serializers import UserCreateSerializer, UserSerializer
from users.models import User
from json import loads, dumps


def register(request):
    request_data = request.POST
    if request.body:
        request_data = loads(request.body.decode('utf-8'))
    user_data = UserCreateSerializer(data=request_data)
    data = None
    if user_data.is_valid():
        user = user_data.save()
        data = {
            'username': user_data.data.get('username'),
            'jwt': get_jwt_for_id(user.id)
        }
    else:
        return StandardResponse(errors=user_data.errors)
    return StandardResponse(data)


def login(request):
    request_data = request.POST
    if request.body:
        request_data = loads(request.body.decode('utf-8'))
    username = request_data.get('username')
    password = request_data.get('password')
    if not username:
        return StandardResponse(errors='username missing')
    try:
        user = User.objects.get(username=username)
        if not check_password(password, user.password):
            return StandardResponse(errors='Password is incorrect')
        else:
            return StandardResponse({
                'username': user.username,
                'jwt': get_jwt_for_id(user.id)
            })
    except Exception:
        return StandardResponse(errors='User does not exist')
