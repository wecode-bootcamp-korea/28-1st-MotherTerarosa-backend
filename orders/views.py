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
    #@login_decorator
    def post(self, requset):

        try:
            cart_data = json.loads(request.body)

            quantity   = cart_data['quantity']
            user       = cart_data['user']
            product_id = cart_data['product_id']

            if not User.objects.filter(user = user).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            if Cart.objects.filter(user=user, product_id = product_id).exists():
                exist_product = Cart.objects.get(user=user, product_id=product_id)
                exist_product.quantity += quantity
                exist_product.save()
                return JsonResponse({'message': 'PRODUCT_ADDED'}, status = 201)

            Cart.objects.create(
                quantity   = quantity,
                user       = user,
                product_id = product_id,
            )

            return JsonResponse({'message': 'PRODUCT_ADDED'}, status = 201)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'INVALID_'}, status=400)            

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

    #@login_decorator
    def get(self, request):
        pass