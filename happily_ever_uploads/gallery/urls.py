from django.urls import path
from .views import ImageListCreateView, ImageDeleteView
from . import views

urlpatterns = [
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),  
    path('images/<int:pk>/delete/', ImageDeleteView.as_view(), name='image-delete'), 
    path('test-upload/', views.test_upload, name='test-upload'),
]
