import re
import jwt

from users.models import User
from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            print(access_token)
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id = payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status = 400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST'}, status = 400)

        return func(self, request, *args, **kwargs)
    return wrapper