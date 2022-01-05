import datetime

from django.http  import JsonResponse
from django.views import View

from products.models import Category, Menu, Product

class ShopListView(View):
    def get(self, request):
        
        query_no = request.GET.get('category_no', None)

        if not query_no:
            return JsonResponse({'message':'INVALID_REQUEST'}, status=400)
        category_no   = ""
        category_name = ""
        products      = ""
        category_id   = 0
        menu_id       = 0

        if query_no == "0":
            products      = Product.objects.all()
        
        else:
            query_separation = str(query_no).split('0')
            category_no      = str(query_no)
            category_name    = ""

            if query_separation[-1]:
                category_id   = query_separation[-1]
                products      = Product.objects.filter(category_id = category_id)
                category_name = Category.objects.get(id=category_id).name

            else:
                menu_id       = query_separation[0]
                products      = Product.objects.filter(menu_id = menu_id)
                category_name = Menu.objects.get(id=menu_id).name
        
        product_list = []
        for product in products:
            target       = Product.objects.get(id=product.id)
            notes        = target.tasting_notes.values()
            price        = int(product.price)
            tasting_note = []
            for note in notes:
                tasting_note.append(note["name"])

            tasting_note_str = ", ".join(tasting_note)

            product_list.append(
                {
                    "id"                  : product.id,
                    "product_name"        : product.name,
                    "price"               : price,
                    "description"         : tasting_note_str,
                    "date"                : product.created_at.strftime("%Y-%m-%d"),
                    "thumbnail_image_url" : product.thumbnail_image_url 
                }
            )
            
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