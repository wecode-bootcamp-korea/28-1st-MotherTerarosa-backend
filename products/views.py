import json

from django.http  import JsonResponse, request
from django.http  import Http404
from django.views import View

from products.models import Product, Category, TastingNote, Image

class ShopListView(View):
    def get(self, request):
        
        query_no = request.GET.get('category_no', None)

        if not query_no:
            return JsonResponse({'message':'INVALID_REQUEST'}, status=400)
        
        query_separation = str(query_no).split('0')

        if query_separation[-1]:
            category_id = query_separation[-1]
            products = Product.objects.filter(category_id = category_id)

        else:
            menu_id     = query_separation[0]
            products = Product.objects.filter(menu_id = menu_id)

        result = []
        for product in products:
            target_product    = Product.objects.filter(id=product.id)
            target_product_pr = target_product.prefetch_related('tasting_notes_set')[0]
            tasting_notes     = target_product_pr.tasting_notes_set.all()
            tasting_note      = [note for note in tasting_notes.name]
            price             = float(product.price)

            result.append(
                {
                    "name"                : product.name,
                    "tasting_notes"       : tasting_note,
                    "price"               : price,
                    "thumbnail_image_url" : product.thumbnail_image_url 
                }
            )
        return JsonResponse({'message':'SUCCESS'}, status=200)