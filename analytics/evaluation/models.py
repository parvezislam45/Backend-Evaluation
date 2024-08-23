# analytics/models.py

from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    def __str__(self):
        return self.city

class Customers(models.Model):
    customer_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    default_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name
    
class Repeat (models.Model):
    customer = models.ForeignKey(Customers, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Product(models.Model):
    product_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any other relevant fields

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other relevant fields

    def __str__(self):
        return self.order_id
    
    
class SalesData(models.Model):
    interval_choices = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=10, choices=interval_choices, default='monthly')
    date = models.DateField()

    def __str__(self):
        return f"{self.interval.capitalize()} Sales on {self.date}: {self.total_sales}"
    
    
class SalesGrowth(models.Model):
    interval_choices = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    growth_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interval = models.CharField(max_length=10, choices=interval_choices, default='monthly')
    date = models.DateField()

    def __str__(self):
        return f"{self.interval.capitalize()} Growth Rate on {self.date}: {self.growth_rate}%"