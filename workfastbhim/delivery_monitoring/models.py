from django.db import models
from datetime import date

class Invoice(models.Model):
    number = models.CharField(max_length=100, default="-")
    si = models.CharField(max_length=100, default="-")
    date = models.DateField(default=date(1991, 1, 25))
    amount = models.FloatField(default=0.0)
    customer_number = models.CharField(max_length=100, default="-")
    customer_name = models.CharField(max_length=200, default="-")
    dispatch_date = models.DateField(null=True, blank=True, default=None)
    delivery_date = models.DateField(null=True, blank=True, default=None)
    remarks = models.TextField(default="-")
    accountable = models.TextField(default="-")
    s_code = models.CharField(max_length=3, default="-")

    def __str__(self):
        return self.number
