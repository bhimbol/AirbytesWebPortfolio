from django.urls import path
from . import views

urlpatterns = [
    path('', views.comments, name='comments'),
    path('command', views.execute_command, name='execute_command'),

]