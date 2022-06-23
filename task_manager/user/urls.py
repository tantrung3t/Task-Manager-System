from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenBlacklistView
from . import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('login/refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    path('profile/mode/', views.ModeApiView.as_view(), name='mode'),
    path('forgot-password/', views.ForgotPasswordApiView.as_view(), name='forgot-password'),
    path('change-password-pin/', views.ChangePasswordWithPINApiView.as_view(), name='change-password-pin'),
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    path('logout/', TokenBlacklistView.as_view(), name='logout')
]