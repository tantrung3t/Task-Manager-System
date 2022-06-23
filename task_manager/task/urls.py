from django.urls import path
from . import views
urlpatterns = [
    path('', views.TaskApiView.as_view(), name='list-task'),
    path('<int:task_id>/', views.DetailTaskApiView.as_view(), name='detail-task')
]