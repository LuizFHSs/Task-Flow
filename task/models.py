from django.db import models
from user.models import CustomUser

# Create your models here.
class Task(models.Model):
    title = models.CharField("Título", max_length=100, blank=False, null=False)
    description = models.TextField("Descrição", blank=True, null=True)
    status = models.CharField("Condição", max_length=10, blank=False, null=False, default="pending")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    completed_at = models.DateTimeField("Finalizada em", auto_now=True)
    