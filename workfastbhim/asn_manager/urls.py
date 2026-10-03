from django.urls import path
from asn_manager import views

app_name = 'asn_manager'
urlpatterns = [
    path('', views.asn_manager_dashboard, name='asn_manager_dashboard'),
    path('login', views.login, name='login'),
    path('initiate_google_auth', views.initiate_google_auth , name='initiate_google_auth'),
    path('logout', views.logout, name='logout'),
    path('auth_callback', views.auth_callback, name='auth_callback'),
    path('view_asn_list', views.view_asn_list, name='view_asn_list'),
    path('download_selected_asn_list', views.download_selected_asn_list, name='download_selected_asn_list'),
    path('consolidate_asn', views.consolidate_asn, name='consolidate_asn'),
    path('checklist', views.checklist, name='checklist'),
]