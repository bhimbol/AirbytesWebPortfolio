from django.urls import path
from my_profile import views

app_name = 'my_profile'
urlpatterns = [
    path('', views.my_profile_dashboard, name='my_profile_dashboard'),
    path('my_gallery', views.my_gallery, name='my_gallery'),
    path('add_image_comment/<int:image_id>/', views.add_image_comment, name='add_image_comment'),
    path('about_page', views.about_page, name='about_page'),
]