
from datetime import datetime
from django.db import models
from user.models import User
from workspace.models import Workspace
# Create your models here.


class Priority(models.Model):
    priority_name = models.CharField(max_length=255)

    def __str__(self):
        return self.priority_name


class Status(models.Model):
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return self.status_name


class Task(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    task_end = models.DateTimeField(null=True)
    task_status = models.ForeignKey(
        Status, on_delete=models.CASCADE, default=1)
    task_description = models.TextField()

    def __str__(self):
        return self.task_name
