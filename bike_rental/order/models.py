from django.db import models
from django.contrib.auth.models import User
from datetime import date
from equipment.models import Accessory, Bike
from django.core.exceptions import ValidationError


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(default=date.today())
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)
    rev_num = models.IntegerField(null=True, default=0)

    order_status = models.CharField(
        max_length=100,
        choices=[
            ('completed', 'completed'), 
            ('in progress', 'in progress'), 
            ('before', 'before'), 
            ('problem', 'problem')
        ],
        default='before'
    )

class BikeItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bike_items')
    equipment = models.ForeignKey(Bike, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if self.quantity < 0:
            raise ValidationError({'quantity': 'Quantity must be greater than or equal to 0.'})

class AccessoryItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='accessory_items')
    equipment = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if self.quantity < 0:
            raise ValidationError({'quantity': 'Quantity must be greater than or equal to 0.'})
