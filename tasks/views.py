from users.serializers import UserSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from tasks.models import Label, Project, Section, Task
from users.models import User
from tasks.serializers import TaskCreateSerializer, TaskSerializer
from todoist.response import resolve_user_id_from_jwt, StandardResponse
from json import loads, dumps
# Create your views here.


class TaskView(APIView):

    def get(self, request):
        try:
            user_id = resolve_user_id_from_jwt(request)
            tasks = Task.objects.filter(user_id=user_id)
            return StandardResponse(TaskSerializer(tasks, many=True).data,)
        except Exception as e:
            return StandardResponse(errors=str(e))

    def post(self, request):
        try:
            user_id = resolve_user_id_from_jwt(request)
            request_data = request.POST
            if request.body:
                request_data = loads(request.body.decode('utf-8'))
            task_serializer = TaskCreateSerializer(
                data={**request_data.dict(), 'user': user_id})
            if not task_serializer.is_valid():
                print(task_serializer.initial_data)
                return StandardResponse(errors=task_serializer.errors)
            else:
                task_id = request_data.get('uuid')
                if task_id:
                    try:
                        task = Task.objects.get(uuid=task_id)
                        project = task.project
                        label = task.label
                        section = task.section
                        parent = task.parent
                        for field in ['project', 'label', 'section', 'parent']:
                            form_data = request_data.get(field)
                            if form_data:
                                if field == 'project':
                                    project = Project.objects.get(pk=form_data)
                                if field == 'label':
                                    label = Label.objects.get(pk=form_data)
                                if field == 'section':
                                    section = Section.objects.get(pk=form_data)
                                if field == 'parent':
                                    parent = Task.objects.get(pk=form_data)
                        task.title = request_data.get('title', task.title)
                        task.project = project
                        task.label = label
                        task.due_date = request_data.get(
                            'due_date', task.due_date)
                        task.priority = request_data.get(
                            'priority', task.priority)
                        task.section = section
                        task.parent = parent
                        task.checked = request_data.get(
                            'checked', task.checked)
                        task.order = request_data.get('order', task.order)
                        task.save()
                    except Exception as e:
                        return StandardResponse(errors=str(e))
                else:
                    task = task_serializer.save(user_id=user_id)
                return StandardResponse(TaskSerializer(task).data)
        except Exception as e:
            return StandardResponse(errors=str(e))


def latest_action(request):
    try:
        user_id = resolve_user_id_from_jwt(request)
        recent_task = Task.objects.filter(user_id=user_id).latest()
        return StandardResponse(recent_task.date_modified)
    except Exception as e:
        return StandardResponse(errors=str(e))
