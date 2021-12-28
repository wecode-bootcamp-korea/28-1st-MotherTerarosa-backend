from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=30)
    username      = models.CharField(max_length=30, unique=True)
    password      = models.CharField(max_length=300)
    address       = models.CharField(max_length=500)
    mobile_number = models.CharField(max_length=50)
    email         = models.CharField(max_length=50, unique=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
