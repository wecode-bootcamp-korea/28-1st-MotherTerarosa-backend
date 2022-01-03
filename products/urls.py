from django.urls    import path

from products.views import ShopListView

urlpatterns = [
    path('/products', ShopListView.as_view())
]