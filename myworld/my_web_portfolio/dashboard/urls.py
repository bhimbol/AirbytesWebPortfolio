from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('val/', views.val, name='val'),
    path('product_details/', views.product_details, name='product_details'),
    path('promo_calculator/', views.promo_calculator, name='promo_calculator'),
    path('upload_pd/', views.upload_pd, name='upload_pd'),
    path('download_selected_attachments/', views.download_selected_attachments, name='download_selected_attachments'),
    path('asn/', views.asn, name='asn'),
    path('asn_process/', views.asn_process, name='asn_process'),
    path('asn_logout/', views.asn_logout, name='asn_logout'),
    path('initiate_google_auth/', views.initiate_google_auth, name='initiate_google_auth'),
    path('callback/', views.callback_view, name='callback_auth'),
]