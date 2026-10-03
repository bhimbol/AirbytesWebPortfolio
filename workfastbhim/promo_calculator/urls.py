from django.urls import path
from promo_calculator import views

app_name = 'promo_calculator'
urlpatterns = [
    path('', views.promo_calculator_dashboard, name='promo_calculator_dashboard'),
    path('calculate', views.calculate, name='calculate'),
]