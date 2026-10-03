from django.urls import path
from image_processor import views

app_name = 'image_processor'
urlpatterns = [
    path('', views.image_processor_dashboard, name='image_processor_dashboard'),
]