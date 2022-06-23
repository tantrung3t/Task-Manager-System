from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from . import serializers
from . import models
from workspace.permissions import IsOwnerWorkspace
from .permissions import IsTaskOfWorkspace



class TaskApiView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerWorkspace]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['task_end', 'task_status__status_name']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_name', 'task_status__id', 'task_end']

    def get_queryset(self):
        self.queryset = models.Task.objects.filter(workspace=self.kwargs['workspace_id'])
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == "GET":
            self.serializer_class = serializers.ReadTaskSerializer
        else:
            self.serializer_class = serializers.WriteTaskSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(workspace=models.Workspace.objects.get(id=self.kwargs['workspace_id']))


class DetailTaskApiView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerWorkspace]
    lookup_url_kwarg = 'task_id'

    def get_queryset(self):
        self.queryset = models.Task.objects.filter(workspace=self.kwargs['workspace_id'])
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ReadTaskSerializer
        else:
            if self.request.method == "PUT" and self.request.data.get('task_status'):   
                    return serializers.ChangeStatusSerializer
            return serializers.WriteTaskSerializer


