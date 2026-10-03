from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_profile.urls', namespace='my_profile')),
    path('asn_manager/', include('asn_manager.urls', namespace='asn_manager')),
    path('product_manager/', include('product_manager.urls', namespace='product_manager')),
    path('promo_calculator/', include('promo_calculator.urls', namespace='promo_calculator')),
    path('receive_sms/', include('sms.urls', namespace='sms')),
    path('sms/', include('sms.urls', namespace='sms')),
    path('image_processor/', include('image_processor.urls', namespace='image_processor')),
    path('delivery_monitoring/', include('delivery_monitoring.urls', namespace='delivery_monitoring')),
    path('price_calculator/', include('price_calculator.urls', namespace='price_calculator')),
    path('loadsheet_script/', include('loadsheet_script.urls', namespace='loadsheet_script')),
    #path('vpet/', include('vpet.urls', namespace='vpet')),
]





