# vpet/urls.py
from django.urls import path
from vpet import views

urlpatterns = []

app_name = 'vpet'
urlpatterns = [
    path('', views.index, name='index'),
]