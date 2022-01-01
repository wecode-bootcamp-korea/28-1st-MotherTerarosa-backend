import json
from json.decoder import JSONDecodeError

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
            cart_data = json.loads(request.body)
            # 유저, 제품, 제품수량
            # 유저 정보에 따라서 user 변수 변경 필요


            if not User.objects.filter(user = cart_data['user']).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            cart_data['product_id']

            Cart.objects.create(
                quantity = cart_data['quantity'],
                user     = cart_data['user'],
                product  = cart_data['product_id'],
            )

            return JsonResponse({'message': 'CREATED'}, status = 201) 

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

    def get(self, request):
        pass