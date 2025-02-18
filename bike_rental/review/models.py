from django.db import models
from django.contrib.auth.models import User
from order.models import Order

class Review(models.Model):
    title = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='review')
    does_exists = models.BooleanField(default=False)
