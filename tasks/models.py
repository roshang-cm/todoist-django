from django.db import models
from users.models import User
# Create your models here.


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=20, blank=True, null=True)


class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Section(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True)


class Task(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)
    label = models.ForeignKey(
        Label, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, blank=True, null=True)
    parent = models.ForeignKey(
        "Task", on_delete=models.SET_NULL, blank=True, null=True)
    checked = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
