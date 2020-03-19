from django.shortcuts import render
from rest_framework.views import APIView
from tasks.models import Task
from users.models import User
from tasks.serializers import TaskSerializer
from todoist.response import resolve_user_id_from_jwt, StandardResponse
# Create your views here.


class TaskView(APIView):

    def get(self, request):
        try:
            user_id = resolve_user_id_from_jwt(request)
            tasks = Task.objects.filter(user_id=user_id)
            return StandardResponse(TaskSerializer(tasks, many=True).data,)
        except Exception as e:
            return StandardResponse(errors=str(e))
