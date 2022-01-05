import jwt

from users.models import User
from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM

def login_decortor(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authrozation', None)
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id = payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status = 400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST'}, status = 400)

        return func(self, request, *args, **kwargs)
    return wrapper