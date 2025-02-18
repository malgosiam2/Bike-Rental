from django.contrib import admin
from .models import AccessoryItem, Order, BikeItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['add'] = False
        return perms


admin.site.register(BikeItem)
admin.site.register(AccessoryItem)