from django.urls import path
from .views import LoginView, UpdateGuestUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Single login for both admin & guest
    path('update-guest/', UpdateGuestUserView.as_view(), name='update-guest'),  # Admin updates guest credentials
]
