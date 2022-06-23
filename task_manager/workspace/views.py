
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
# Create your views here.
from workspace.serializers import ReadWorkspaceSerializer, WriteWorkspaceSerializer, UploadImageWorkspace
from workspace.models import Workspace
from workspace.permissions import IsOwnerWorkspace

# Create your views here.


class ListCreateWorkspaceApiView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReadWorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.filter(user=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = WriteWorkspaceSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):

        data = {
            "title": request.data.get('title'),
            "description": request.data.get('description'),
            "user": request.user.id
        }

        if request.data.get('image') is not None:
            data['image'] = request.data.get('image')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateWorkspaceApiView(generics.RetrieveUpdateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerWorkspace]
    serializer_class = UploadImageWorkspace
    queryset = Workspace.objects.all()
    lookup_url_kwarg = 'workspace_id'
