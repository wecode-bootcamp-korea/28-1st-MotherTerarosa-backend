from django.http  import JsonResponse
from django.views import View

from products.models import Product, Menu, Category

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

class ProductListView(View):
    def concat_notes(self, notes_list):
        return ', '.join(notes_list)

    def get(self, request):
        
        category = request.GET.get('category', None)

        products         = Product.objects.all()
        query_separation = str(category).split('0')
        category_no      = str(category)
        category_name    = ""

        if query_separation[-1]:
            category_id   = query_separation[-1]
            products      = Product.objects.filter(category_id = category_id)
            category_name = Category.objects.get(id=category_id).name

        else:
            menu_id       = query_separation[0]
            products      = Product.objects.filter(menu_id = menu_id)
            category_name = Menu.objects.get(id=menu_id).name
        
        product_list = [{
            "id"                  : product.id,
            "product_name"        : product.name,
            "price"               : int(product.price),
            "description"         : self.concat_notes([note.name for note in product.tasting_notes.all()]),
            "date"                : product.created_at.strftime("%Y-%m-%d"),
            "thumbnail_image_url" : product.thumbnail_image_url 
        } for product in products]
            
        result = {
            "category_no"   : category_no,
            "category_name" : category_name,
            "products"      : product_list
        }
        
        return JsonResponse({'result':result}, status=200)

class CategoryView(View):
    def get(self, request):
        categories = []
        menus_list = Menu.objects.all()

        for menu_obj in menus_list:
            menu_no         = str(menu_obj.id)+"00"
            menu_name       = menu_obj.name
            categories_list = menu_obj.category_set.all()
            sub_categories  = []
            sub_categories  = [
                {
                    "no"   : menu_no+"00"+str(sub_category.id),
                    "name" : sub_category.name
                } for sub_category in categories_list if categories_list != []
            ]
            categories.append(
                {
                    "no"             : menu_no,
                    "name"           : menu_name,
                    "sub_categories" : sub_categories
                }
            )
            
        return JsonResponse({'result':categories}, status=200)