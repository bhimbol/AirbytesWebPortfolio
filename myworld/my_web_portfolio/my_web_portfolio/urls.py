from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('dashboard.urls')),
	path('', include('sendSMS.urls')),
	path('dashboard/', include('dashboard.urls')),
	path('about/', include('dashboard.urls')),
	path('comments/', include('comments.urls')),
	path('gallery/', include('gallery.urls')),
	path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


