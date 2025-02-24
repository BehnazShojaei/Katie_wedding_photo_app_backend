from django.urls import path
from .views import ImageListCreateView, ImageDetailView, ImageDeleteView

urlpatterns = [
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),  
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),  
    path('images/<int:pk>/delete/', ImageDeleteView.as_view(), name='image-delete'), 
]
