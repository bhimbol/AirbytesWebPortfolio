from django.urls import path
from delivery_monitoring import views

app_name = 'delivery_monitoring'
urlpatterns = [
    path('', views.delivery_monitoring_dashboard, name='delivery_monitoring_dashboard'),
    path('delivery_planning', views.DeliveryPlanning, name='delivery_planning'),
    path('create_plan', views.create_plan, name='create_plan'),
]