from django.urls import path
from .views import LoginView, UpdateGuestUserView, ChangeAdminPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Single login for both admin & guest
    path('update-guest/', UpdateGuestUserView.as_view(), name='update-guest'),  # Admin updates guest credentials
    path('change-password/', ChangeAdminPasswordView.as_view(), name='change-password'),  # Admin changes their password

]
