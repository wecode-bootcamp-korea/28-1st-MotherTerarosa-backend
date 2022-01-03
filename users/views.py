import json
import re
import bcrypt

from django.views import View
from django.http  import JsonResponse

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username      = data['username']
            password      = data['password']
            name          = data['name']
            email         = data['email']

            username_regex = '^[a-z0-9]{4,16}$'
            password_regex = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            email_regex    = '[a-zA-Z0-9.-_+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+'

            if not re.match(username_regex, username):
                return JsonResponse({'message': 'INVALID_USERNAME'}, status = 400)

            if not re.match(password_regex, password):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)

            if not re.match(email_regex, email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)    

            if User.objects.filter(username = username).exists():
                return JsonResponse({'message': 'ALREADY_EXIST_USERNAME'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message': 'ALREADY_EXIST_EMAIL'}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username      = username,
                password      = hashed_password,
                name          = name,
                email         = email
            )
            return JsonResponse({'messege': 'CREATE ACCOUNT SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)