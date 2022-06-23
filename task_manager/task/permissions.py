from rest_framework import permissions
from .models import Task

class IsTaskOfWorkspace(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            task = Task.objects.get(id = view.kwargs.get('task_id'))
        except:
            return False
        return bool(task.workspace.id == view.kwargs.get('workspace_id'))