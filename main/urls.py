from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup, name='signup'),
    path('fetch_booking/', views.fetch_booking, name='fetch_booking'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('ping_server/', views.ping_server, name='ping_server'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]