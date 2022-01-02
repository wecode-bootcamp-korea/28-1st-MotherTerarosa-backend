import json
from json.decoder import JSONDecodeError

from django.http             import JsonResponse, request
from django.views            import View
from django.core.exceptions  import ValidationError

from orders.models   import Order,Order_Product,OrderStatus
from products.models import Cart
from users.models    import User
from utils.login_decorator import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            cart_data = json.loads(request.body)

            user_id    = request.id
            quantity   = cart_data['quantity']
            product_id = cart_data['product_id']

            if int(quantity)<1 :
                return JsonResponse({'massage': 'QUANTITY_UNSELECTED'}, status = 400)

            cart, created = Cart.objects.get_or_create(
                user_id    = user_id,
                product_id = product_id
            )
            cart.quantity += quantity
            cart.save()

            return JsonResponse({'message': 'PRODUCT_ADD'}, status = 201)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'INVALID_CART'}, status=400)            

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)