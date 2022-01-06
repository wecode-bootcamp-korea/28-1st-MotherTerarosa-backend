import json

from django.http  import JsonResponse
from django.views import View
from json.decoder import JSONDecodeError

from orders.models         import Order,Order_Product,OrderStatus
from products.models       import Cart, Product
from users.models          import User
from utils.login_decorator import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']

            cart, created  = Cart.objects.get_or_create(
                user_id    = user.id,
                product_id = product_id
            )
            cart.quantity += quantity
            cart.save()
            return JsonResponse({'message': 'CREATE_CART_SUSSESS'}, status = 201)
        
        except KeyError:
            JsonResponse({'message': 'KEY_ERROR'}, status = 400)
            
        except JSONDecodeError:
            return JsonResponse({'message': 'JsonDecodeError'}, status = 400)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_NOT_EXIST'}, status = 404)    

    @login_decorator
    def get(self, request):

        user   = request.user
        carts  = Cart.objects.select_related('product').filter(user = user)
        result = []

        for cart in carts:
            result.append({
                'cart_id'            : cart.id,
                'product_id'         : cart.product.id,
                'product_name'       : cart.product.name,
                'thumbnail_image_url': cart.product.thumbnail_image.url,
                'price'              : cart.product.price,
                'quantity'           : cart.quantity
            })

        return JsonResponse({'result': result}, status = 200)
       
    @login_decorator
    def delete(self, request):
       
        data = json.loads(request.body)

        user = request.user
        cart = Cart.objects.get(id = data['cart_id'], user = user)
            
        if not Cart.objects.filter(id = data['cart_id'], user = user).exists():
            return JsonResponse({'message': 'NOT_EXIST'}, status = 400)
            
        cart.delete()

        return JsonResponse({'message': 'DELETE_CART_SUCCESS'}, status = 204)