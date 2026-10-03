from django.urls import path
from product_manager import views

app_name = 'product_manager'
urlpatterns = [
    path('', views.product_manager_dashboard, name='product_manager_dashboard'),
    path('update_file', views.update_file, name='update_file'),
    path('export_poduct_details', views.export_poduct_details, name='export_poduct_details'),
    path('export_recon', views.export_recon, name='export_recon'),

]