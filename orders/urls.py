from django.urls import path

from orders.views import CartView, OrderView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/orderitem', OrderView.as_view())
]
