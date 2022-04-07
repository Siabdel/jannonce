from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

urlpatterns = [

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls, name='admin'), # console admin
    path('wejob/', include('wejob.urls')),
    # module allaccount
    path('accounts/', include('allauth.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
