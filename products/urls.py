from django.urls import path
from products.views import MainView, ProductDetailView, ShopListView, CategoryView

urlpatterns = [
    path('', ShopListView.as_view()),
    path('/categories', CategoryView.as_view()),
    path('/productdetail/<int:product_id>', ProductDetailView.as_view()),
    path('/main', MainView.as_view())
]