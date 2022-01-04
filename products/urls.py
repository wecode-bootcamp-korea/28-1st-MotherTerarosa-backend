from django.urls    import path

from products.views import ShopListView, CategoryView

urlpatterns = [
    path('', ShopListView.as_view()),
    path('/categories', CategoryView.as_view()), 
]