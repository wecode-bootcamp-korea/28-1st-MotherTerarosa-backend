from django.http  import JsonResponse
from django.views import View
from django.db.models import Q

from products.models import Product, Menu, Category

class MainView(View):
    def get(self, request):
        try:
            query_best = Product.objects.all().order_by("-product_hits")[0:3]
            query_new  = Product.objects.all().order_by("created_at")[0:4]

            data = [{
                "categoryName" : "BEST",
                "products" : [{
                    "id" : best.id,
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
                    "id" : new.id,
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

class ProductListView(View):
    def concat_notes(self, notes_list):
        return ', '.join(notes_list)

    def get(self, request):
        try:
            category = request.GET.get('category', None)
            
            menu_id       = ''
            category_id   = ''
            category_name = 'shop'

            if category:
                menu_id     = category[:3].rstrip('0')
                category_id = category[3:].lstrip('0')

            q = Q()

            if menu_id:
                q &= Q(menu_id = menu_id)
                category_name = Menu.objects.get(id=menu_id).name

            if category_id:
                q &= Q(category_id = category_id)
                category_name = Category.objects.get(id=category_id).name

            products = Product.objects.filter(q)

            product_list = [{
                "id"                  : product.id,
                "product_name"        : product.name,
                "price"               : int(product.price),
                "description"         : self.concat_notes([note.name for note in product.tasting_notes.all()]),
                "date"                : product.created_at.strftime("%Y-%m-%d"),
                "thumbnail_image_url" : product.thumbnail_image_url 
            } for product in products]
                
            result = {
                "category"      : category,
                "category_name" : category_name,
                "products"      : product_list
            }

            return JsonResponse({'result': result}, status=200)

        except Menu.DoesNotExist:
            return JsonResponse({'message': 'MENU_DOES_NOT_EXIST'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=400)

class CategoryView(View):
    def append_sub_categories(self, menu, categories): 
        sub_categories = [
                {
                    "no"   : str(menu.id)+"0000"+str(sub_category.id),
                    "name" : sub_category.name
                } for sub_category in categories if categories != []
            ]
            
        return sub_categories

    def get(self, request):
        result = []
        menus = Menu.objects.all()
        
        for menu in menus:
            categories     = menu.category_set.all()

            result.append(
                {
                    "no"             : str(menu.id)+"00",
                    "name"           : menu.name,
                    "sub_categories" : self.append_sub_categories(menu, categories)
                }
            )

        return JsonResponse({'result':result}, status=200)