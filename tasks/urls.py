from django.urls import path
from .views import (
    TaskCreateView,
    TaskListView,
    TaskRetrieveView,
    TaskUpdateView,
    TaskDestroyView,
)

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('list/', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskRetrieveView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDestroyView.as_view(), name='task-delete'),
]
