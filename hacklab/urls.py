from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from hacklab import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', direct_to_template, {'template':'index.html'}, name="mainpage"),
	(r'^no_permission/$', direct_to_template, {'template':'account/noperm.html'}),
	(r'^biblioteka', include('hacklab.biblioteka.urls')),
	(r'^registration', include('hacklab.registration.urls')),
	(r'^account', include('hacklab.registration.urls2')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_PATH+'/media'}),

)
