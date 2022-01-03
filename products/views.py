import json

from django.http      import JsonResponse, request
from django.views     import View

from products.models    import Product, Category, TastingNote, Image

class ShopListView(View):
    def get(self, request):
        

        return

