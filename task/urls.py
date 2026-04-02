from django.urls import path
from .views import create_task, list_task, list_task_by_user, mark_task_completed, delete_task

urlpatterns = [
    path('create_task/', create_task, name="create_task"),
    path('list_tasks/', list_task, name="list_tasks"),
    path('list_user_task/', list_task_by_user, name="list_user_task"),
    path('mark_task/', mark_task_completed, name="mark_task"),
    path('delete_task/', delete_task, name="delete_task"),
]
