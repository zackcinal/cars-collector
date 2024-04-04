from django.contrib import admin
from .models import Car, Fueling, Accessory
# Register your models here.

admin.site.register(Car)
admin.site.register(Fueling)
admin.site.register(Accessory)