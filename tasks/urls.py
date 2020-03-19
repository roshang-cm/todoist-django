from django.urls import include, path
from tasks import views

urlpatterns = [
    path('', views.TaskView.as_view()),
]
