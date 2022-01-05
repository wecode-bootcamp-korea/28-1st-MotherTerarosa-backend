import json
import datetime

from django.http      import JsonResponse, request
from django.views     import View

from products.models    import Product, TastingNote, Image

class MainView(View):
    def get(self, request):
        try:
            query_best = Product.objects.all().order_by("-product_hits")[0:3]
            query_new = Product.objects.all().order_by("created_at")[0:4]

            data = [{
                "categoryName" : "BEST",
                "products" : [{
                    "id" : str(best.id),
                    "name" : best.name,
                    "price" : int(best.price),
                    "tasting_note" : [taste.name for taste in best.tasting_notes.all()],
                    "description" : "",
                    "image_url" : best.thumbnail_image_url,
                    "created_at" : best.created_at.strftime('%Y-%m-%d')
                } for best in query_best]},
                {
                "categoryName" : "NEW",
                "products" : [{
                    "id" : str(new.id),
                    "name" : new.name,
                    "price" : int(new.price),
                    "tasting_note" : [taste.name for taste in new.tasting_notes.all()],
                    "description" : "",
                    "image_url" : new.thumbnail_image_url,
                    "created_at" : new.created_at.strftime('%Y-%m-%d')
                } for new in query_new]
            }]

            return JsonResponse({"result" : data}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "NOT_FOUND"}, status=400)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            image = product.image_set.all()

            data = {
                "name" : product.name,
                "description" : product.description,
                "price" : int(product.price),
                "image_url" : [i.image_url for i in image]
            }
            return JsonResponse({'result' : data}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'NOT_FOUND'}, status=400)