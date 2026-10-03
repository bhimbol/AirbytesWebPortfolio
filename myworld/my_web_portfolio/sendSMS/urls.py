from django.urls import path
from .views import send_sms, receive_sms

urlpatterns = [
    path('receive_sms/', receive_sms, name='receive_sms'),
    path('send_sms/', send_sms, name='send_sms'),
]