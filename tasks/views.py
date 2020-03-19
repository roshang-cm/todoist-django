from django.shortcuts import render
from rest_framework.views import APIView
from tasks.models import Label, Project, Section, Task
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

    def post(self, request):
        try:
            user_id = resolve_user_id_from_jwt(request)
            task_serializer = TaskSerializer(
                data={**request.data.dict(), 'user': user_id})
            if not task_serializer.is_valid():
                print(task_serializer.initial_data)
                return StandardResponse(errors=task_serializer.errors)
            else:
                task_id = request.data.get('task_id')
                if task_id:
                    try:
                        task = Task.objects.get(pk=task_id)
                        project = task.project
                        label = task.label
                        section = task.section
                        parent = task.parent
                        for field in ['project', 'label', 'section', 'parent']:
                            form_data = request.POST.get(field)
                            if form_data:
                                if field == 'project':
                                    project = Project.objects.get(pk=form_data)
                                if field == 'label':
                                    label = Label.objects.get(pk=form_data)
                                if field == 'section':
                                    section = Section.objects.get(pk=form_data)
                                if field == 'parent':
                                    parent = Task.objects.get(pk=form_data)
                        task.title = request.POST.get('title', task.title)
                        task.project = project
                        task.label = label
                        task.due_date = request.POST.get(
                            'due_date', task.due_date)
                        task.priority = request.POST.get(
                            'priority', task.priority)
                        task.section = section
                        task.parent = parent
                        task.checked = request.POST.get(
                            'checked', task.checked)
                        task.order = request.POST.get('order', task.order)
                        task.save()
                    except Exception as e:
                        return StandardResponse(errors=str(e))
                else:
                    task = task_serializer.save(user_id=user_id)
                return StandardResponse(TaskSerializer(task).data)
        except Exception as e:
            return StandardResponse(errors=str(e))
