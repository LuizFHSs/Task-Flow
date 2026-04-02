from django.db import models

# Create your models here.
class CustomUser(models.Model):
    name = models.CharField("Nome",max_length=100, blank=False, null=False)
    email = models.EmailField("Email", max_length=254, blank=False, null=False, unique=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)