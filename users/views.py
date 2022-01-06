import json
import re
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from my_settings  import ALGORITHM, SECRET_KEY
from users.models import User
from datetime     import datetime, timedelta

class SignUpView(View):
    def validate_user_input(self, username, password, email):
        username_regex = '[a-z0-9]{4,16}'
        password_regex = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        email_regex    = '[a-zA-Z0-9.-_+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+'

        if not re.match(username_regex, username):
            raise ValidationError
            # return JsonResponse({'message': 'INVALID_USERNAME'}, status = 400)

        if not re.match(password_regex, password):
            # return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)

        if not re.match(email_regex, email):
            # return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)

    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']
            password = data['password']
            name     = data['name']
            email    = data['email']

            self.validate_user_input(username, password, email)

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return JsonResponse({'message': 'ALREADY_EXIST_USERNAME'}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username = username,
                password = hashed_password,
                name     = name,
                email    = email
            )
            return JsonResponse({'messege': 'CREATE ACCOUNT SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except ValidationError:
            return JsonResponse(...)

class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(username = data['username'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_USER'}, status = 400)

            payload = {'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=3)}
            access_token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({'message': 'LOGIN SUCCESS', 'token': access_token}, status = 200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status = 404)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)