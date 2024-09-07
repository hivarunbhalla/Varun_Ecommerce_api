from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


#ADMIN SITE 
admin.site.site_header = "Shop ADMIN"
admin.site.index_title = "Admin"



urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    
    # Auth with Djoser and JWT
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
