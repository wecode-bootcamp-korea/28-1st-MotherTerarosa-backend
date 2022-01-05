import json
from json.decoder import JSONDecodeError

from django.http             import JsonResponse, request
from django.views            import View
from django.core.exceptions  import ValidationError

from orders.models   import Order,Order_Product,OrderStatus
from products.models import Cart, Product
from users.models    import User
#from utils.login_decorator import login_decorator

class CartView(View):
 #   @login_decorator
    def post(self, request):
        try:
            cart_data = json.loads(request.body)
            print(cart_data)
            user = User.objects.get(id=1)
            #user       = request.user_id #토큰값으로 받게 되있다.
            quantity   = cart_data['quantity']
            product_id = cart_data['product_id']


            cart, created  = Cart.objects.get_or_create(
                user       = user,
                product_id = product_id
            )
            cart.quantity += quantity
            cart.save()

            if cart.quantity < 1:
                return JsonResponse({'message': 'QUANTITY_UNSELECTED'}, status = 400)

            return JsonResponse({'message': 'PRODUCT_ADD'}, status = 201)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'INVALID_CART'}, status=400)            

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

    #@login_decorator
    def get(self, request):
        try:
            cart = Cart.objects.get(id = cart.id)
            user = User.objects.get(id = user.id)
            product = Product.objects.get(id = product.id)

            data = {
                'cart_id': cart.id,
                'user_id': user.id,
                'product_id': product.id,
                'quantity': cart.quantity,
                'price': product.price * cart.quantity
            }

            return JsonResponse({'result': data}, status = 200)
        except:
            pass

    #@login_decorator
    def delete(self, request):
        try:
            cart_data = json.loads(request.body)

            cart_id = cart_data['cart_id']
            user = request.user
            
            if not Cart.objects.filter(cart_id = cart_id, user = user).exists():
                return JsonResponse({'message': 'NOT_EXIST'})
            
           
            cart_id.delete()

        except: 
            return JsonResponse({'message': 'DELETE_CART_SUCCESS'})
