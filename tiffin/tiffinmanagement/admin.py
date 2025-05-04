from django.contrib import admin
from .models import Customers, MealOptions, Extras, daily_records
# Register your models here.

admin.site.register(Customers)
admin.site.register(MealOptions)
admin.site.register(Extras)
admin.site.register(daily_records)