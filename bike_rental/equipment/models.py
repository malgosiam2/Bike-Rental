from django.db import models
from django.forms import ValidationError

class Equipment(models.Model):
    
    class Meta:
        abstract = True

    price_for_one_day = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="equipment/")
    quantity = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=100)
    additional_info = models.CharField(max_length=500, blank=True, null=True)
    person = models.CharField(max_length=100, choices= [
        ('Men', 'Men'), ('Women', 'Women'), ('Kids', 'Kids'), ('Unisex', 'Unisex')], default='Unisex')
    
    def clean(self):
        if self.price_for_one_day <= 0:
            raise ValidationError({'price_for_one_day': 'Price must be greater than 0!'})

class Bike(Equipment):
    bike_type = models.CharField(max_length=100)
    gear_num = models.PositiveIntegerField()
    usage = models.CharField(max_length=100)
    has_bell = models.BooleanField(default=False)
    has_trunk = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    wheel_size_cm = models.DecimalField(max_digits=4, decimal_places=2)
    brake_type = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.bike_type

class Accessory(Equipment):
    accessory_type = models.CharField(max_length=50)

    def __str__(self):
        return self.accessory_type