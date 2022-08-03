from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AuthUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete = models.CASCADE)
    def __str__(self) -> str:
        return self.name
