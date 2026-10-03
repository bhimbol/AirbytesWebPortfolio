from django.urls import path
from sms import views

app_name = 'sms'
urlpatterns = [
    path('', views.receive_sms, name='receive_sms'),
    path('send_sms', views.send_sms, name='send_sms'),
]