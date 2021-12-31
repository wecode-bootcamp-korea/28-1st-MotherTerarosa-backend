import json
from json.decoder import JSONDecodeError
from os import stat_result

from django.http   import JsonResponse, request
from django.views  import View

from orders.models   import (
    Order,
    Order_Product,
    OrderStatus
)
from products.models import (
    Menu,
    Category,
    Product,
    TastingNote,
    Image,
    ProductStock,
    Cart
)
from users.models    import User

class CartView(View):
    def post(self, requset):

        try:
            data = json.loads(request.body)

            if not User.objects.filter(user = data['user']).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            carts = Cart.objects.create(
                quantity = data['quantity'],
                user     = data['user'],
                product  = data['product_id'],
            )

            return JsonResponse({'message': 'CREATED'}, status = 201) 

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

    def get(self, request):
        pass