from django.db import models

from products.models import Product
from users.models    import User

class Order(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    order_status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)
    price        = models.DecimalField(max_digits=9 , decimal_places=2)
    quantity     = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    products     = models.ManyToManyField(Product, through="Order_Product")

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'orderstatuses'

class Order_Product(models.Model):
    order   = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders_products'