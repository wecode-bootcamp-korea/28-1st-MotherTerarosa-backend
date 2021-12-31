from django.urls import path
from django.urls.conf import path, include

urlpatterns = [
    path('users', include('users.urls'))
]
