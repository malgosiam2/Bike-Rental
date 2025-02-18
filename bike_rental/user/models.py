from django.db import models
from django.contrib.auth.models import User

class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=64)
    is_confirmed = models.BooleanField(default=False)