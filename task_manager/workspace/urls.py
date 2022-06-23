
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListCreateWorkspaceApiView.as_view(), name="workspace"),
    path('<int:workspace_id>/', views.UpdateWorkspaceApiView.as_view(), name='update-workspace'),
    path('<int:workspace_id>/task/', include("task.urls"))
]