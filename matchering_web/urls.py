from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('mgw_front.urls')),
    path('api/', include('mgw_back.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
