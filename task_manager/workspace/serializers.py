from dataclasses import fields
from .models import Workspace
from rest_framework.serializers import ModelSerializer

class ReadWorkspaceSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'title', 'description', 'image']

class WriteWorkspaceSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class UploadImageWorkspace(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['image']