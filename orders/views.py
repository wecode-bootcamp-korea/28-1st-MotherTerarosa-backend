import json
from json.decoder import JSONDecodeError
from django import views

from django.http             import JsonResponse
from django.views            import View
from django.core.exceptions  import ValidationError

from orders.models   import Order,Order_Product,OrderStatus
from products.models import Cart, Product
from users.models    import User
from utils.login_decorator import login_decortor

class CartView(View):
    @login_decortor
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user
            product_id = Product.objects.get(id = data['product_id'])
            quantity = data['quantity']

            cart, created = Cart.objects.get_or_create(
                user_id = user.id,
                product_id = product_id
            )
            cart.quantity += quantity
            cart.save()
            return JsonResponse({'message': 'CREATE_CART_SUSSESS'}, status = 201)

        except KeyError:
            JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    @login_decortor
    def get(self, request):

        user = request.user
        carts = Cart.objects.select_related('product').filter(user = user)
        result = []

        for cart in carts:
            result.append({
                'cart_id': cart.id,
                'product_id': cart.product.id,
                'product_name': cart.product.name,
                'thumbnail_image_url': cart.product.thumbnail_image.url,
                'price': cart.product.price,
                'quantity': cart.quantity
            })

        # data = [{
        #     'cart_id': cart.id,
        #     'product_id': cart.product.id,
        #     'product_name': cart.product.name,
        #     'thumbnail_image_url': cart.product.thumbnail_image.url,
        #     'price': cart.product.price,
        #     'quantity': cart.quantity
        # } for cart in carts]

        return JsonResponse({'result': result}, status = 200)
       
    @login_decortor
    def delete(self, request):
        # try:
            data = json.loads(request.body)

            user = request.user
            cart = Cart.objects.get(id = data['cart_id'], user = user)
            
            if not Cart.objects.filter(id = data['cart_id'], user = user).exists():
                return JsonResponse({'message': 'NOT_EXIST'})
            
            cart.delete()
            return JsonResponse({'message': 'DELETE_CART_SUCCESS'}, status = 204)

        # except: 
        #     return JsonResponse({'message': 'DELETE_CART_SUCCESS'}, status = 204)

  


# class CartView(View):
#     @login_decortor
#     def post(self, request):
#         try:
#             cart_data = json.loads(request.body)
#             print(cart_data)
#             user = User.objects.get(id=1)
#             #user       = request.user_id #토큰값으로 받게 되있다.
#             quantity   = cart_data['quantity']
#             product_id = cart_data['product_id']


#             cart, created  = Cart.objects.get_or_create(
#                 user       = user,
#                 product_id = product_id
#             )
#             cart.quantity += quantity
#             cart.save()

#             if cart.quantity < 1:
#                 return JsonResponse({'message': 'QUANTITY_UNSELECTED'}, status = 400)

#             return JsonResponse({'message': 'PRODUCT_ADD'}, status = 201)

#         except Cart.DoesNotExist:
#             return JsonResponse({'message': 'INVALID_CART'}, status=400)            

#         except KeyError:
#             return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
#         except JSONDecodeError:
#             return JsonResponse({'message': 'JSONDecodeError'}, status=400)

#     @login_decortor
#     def get(self, request):
#         try:
#             cart = Cart.objects.get(id = cart.id)
#             user = User.objects.get(id = user.id)
#             product = Product.objects.get(id = product.id)

#             data = {
#                 'cart_id': cart.id,
#                 'user_id': user.id,
#                 'product_id': product.id,
#                 'quantity': cart.quantity,
#                 'price': product.price * cart.quantity
#             }

#             return JsonResponse({'result': data}, status = 200)
#         except:
#             pass
