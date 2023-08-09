from django.db import models
from django.utils.timezone import now
from farmer.models import Products as Farmer_Products

# Create your models here.
class Registration(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    firstname = models.CharField(max_length=100, default='null', null=False)
    lastname = models.CharField(max_length=100, default='null', null=False)
    email = models.CharField(max_length=255, default='null', null=False)
    password = models.CharField(max_length=500, default='null', null=False)
    mobilenumber = models.CharField(max_length=15, default='null', null=False)
    address = models.TextField(default='null', null=False)
    status_choices = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="active")
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.email

class ShoppingCart(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    public_user=models.ForeignKey(Registration, on_delete=models.CASCADE, default=0,)
    products=models.ForeignKey(Farmer_Products, on_delete=models.CASCADE, default=0,)
    quantity=models.IntegerField(default=0, null=False)
    date_added = models.DateTimeField(default=now, editable=False)
