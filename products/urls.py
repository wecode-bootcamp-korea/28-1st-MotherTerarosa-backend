from django.urls import path

from products.views import MainView, ProductDetailView

urlpatterns = [
    path('/productdetail/<int:product_id>', ProductDetailView.as_view()),
    path('/main', MainView.as_view())
]