from django.urls import path
from orders.views import OrderView
urlpatterns = [
    path('/orderitem', OrderView.as_view())
]