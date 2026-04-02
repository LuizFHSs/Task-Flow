from django.urls import path
from .views import task_handler, task_detail_or_delete, mark_task_completed

urlpatterns = [
    path('', task_handler),
    path('<int:id>/', task_detail_or_delete),
    path('<int:id>/complete/', mark_task_completed, name="mark_task_completed"),
]
