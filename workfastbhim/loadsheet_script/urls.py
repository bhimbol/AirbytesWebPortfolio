from django.urls import path
from . import views

app_name = 'loadsheet_script'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('consolidate_invoices_from_loadsheets/', views.consolidate_invoices_from_loadsheets, name='consolidate_invoices_from_loadsheets'),
]