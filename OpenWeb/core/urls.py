from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('', views.upload_pdf, name='upload_pdf'),
    path('upload/', views.upload_folder, name='ind'),
]
