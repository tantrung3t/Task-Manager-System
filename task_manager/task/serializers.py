from dataclasses import field, fields
from xml.parsers.expat import model
from rest_framework.serializers import ModelSerializer
from .models import Task


class ReadTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "task_name", "created", "updated", "task_end",
                  "task_description", "task_priority", "task_status"]
        depth = 1

class WriteTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        exclude = ['workspace']

class ChangeStatusSerializer(ModelSerializer):
    class Meta:
        model=Task
        fields=["task_status"]