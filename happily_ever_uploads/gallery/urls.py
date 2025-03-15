from django.urls import path
from .views import ImageListCreateView, ImageDeleteView, ImageDetailView, ImageDownloadView, ExportDataView
from . import views

urlpatterns = [
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),  
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-delete'), 
    path('images/delete/<int:pk>/', ImageDeleteView.as_view(), name='image-delete'), 
    path('images/<int:pk>/download/', ImageDownloadView.as_view(), name='image-download'),
    path('images/export-data/', ExportDataView.as_view(), name='export-data'),
    path('test-upload/', views.test_upload, name='test-upload'),
]
