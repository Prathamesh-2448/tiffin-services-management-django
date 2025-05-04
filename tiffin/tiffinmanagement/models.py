from django.db import models

# Create your models here.
class Customers(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=11)
    address = models.CharField(max_length=355)

    def __str__(self):
        return self.name

class MealOptions(models.Model):
    MealName = models.CharField(max_length=50)
    MealPrice = models.IntegerField()

    def __str__(self):
        return self.MealName

class Extras(models.Model):
    ExtraName = models.CharField(max_length=50)
    ExtraPrice = models.IntegerField()

    def __str__(self):
        return self.ExtraName

class daily_records(models.Model):
    customer_name = models.CharField(max_length=100)
    meal_date = models.DateField()
    meal_selected = models.CharField(max_length=100)
    meal_price = models.DecimalField(max_digits=10, decimal_places=2)
    extras_taken = models.TextField()  # Store as comma-separated string
    extras_quantities = models.TextField()  # Store as comma-separated string
    extras_total_price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return f"Order by {self.customer_name} - {self.total_price} on {self.meal_date}"