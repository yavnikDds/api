from django.urls import path
from .views import hello_world, register_user, login_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
]