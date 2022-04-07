from django.conf.urls import  include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'jannonces.views.home', name='home'),
    # url(r'^jannonces/', include('jannonces.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls), name='admin'), # console admin
    url(r'^wejob/', include('wejob.urls')),
    # module allaccount
    url(r'^accounts/', include('allauth.urls')),

]
