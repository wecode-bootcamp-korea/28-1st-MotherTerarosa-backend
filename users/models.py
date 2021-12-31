from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=30)
    username      = models.CharField(max_length=30, unique=True)
    password      = models.CharField(max_length=300)
    address       = models.CharField(max_length=500, blank=True)
    mobile_number = models.CharField(max_length=50, blank=True)
    email         = models.CharField(max_length=50, unique=True)
    point         = models.DecimalField(max_digits=9, decimal_places=2, default=1000000)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
