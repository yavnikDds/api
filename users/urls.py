from django.urls import path
from .views import hello_world, register_user, login_user

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user')
]