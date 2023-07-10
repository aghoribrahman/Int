from django.urls import path
from ppt import views

urlpatterns = [
    # Other URL patterns...
    path('', views.upload_excel, name='upload_excel'),
]
