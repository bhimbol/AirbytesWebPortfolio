from django.urls import path
from price_calculator import views

app_name = 'price_calculator'
urlpatterns = [
    path('', views.price_calculator_dashboard, name='price_calculator_dashboard'),
]