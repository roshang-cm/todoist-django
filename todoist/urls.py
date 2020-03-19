from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from users import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register),
    path('login', views.login),
    path('tasks/', include('tasks.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
