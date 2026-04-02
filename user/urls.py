from django.urls import path
from .views import users_handler, list_tasks_by_user

urlpatterns = [
    path('', users_handler),
    path('<int:id>/tasks/', list_tasks_by_user, name="list_tasks_by_user"),
]