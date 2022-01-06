import uuid

from django.db import models

from products.models import Product
from users.models    import User

class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_price  = models.DecimalField(max_digits=9 , decimal_places=2)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)
    products     = models.ManyToManyField(Product, through="Order_Product")

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'orderstatuses'

class Order_Product(models.Model):
    order       = models.ForeignKey("Order", on_delete=models.CASCADE, null=True) # FIXME Add : null=True
    quantity    = models.IntegerField()
    total_price = models.DecimalField(max_digits=9 , decimal_places=2)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders_products'