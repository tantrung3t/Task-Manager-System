
from rest_framework import permissions
from .models import Workspace

class IsOwnerWorkspace(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            workspace = Workspace.objects.get(id = view.kwargs.get('workspace_id'))
        except:
            return False
        return bool(request.user.id == workspace.user.id)