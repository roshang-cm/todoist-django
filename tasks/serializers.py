from users.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer
from tasks.models import Task


class TaskSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        depth = 1


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1
