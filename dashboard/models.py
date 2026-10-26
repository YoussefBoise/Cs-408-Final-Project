
from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=30)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_amount = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_amount


class Event(models.Model):
    STATUS_CHOICES = [
        ('Nt Apot Applied', 'Noplied'),
        ('Applied', 'Applied'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Attending', 'Attending'),
    ]

    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    application_deadline = models.DateField()
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    application_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Not Applied'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()


class Expense(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_amount
    
