from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, password_reset_done


urlpatterns = patterns('hacklab.registration.views',
	(r'^/$', 'register'),
	url(r'^/success/$', direct_to_template, {'template': 'registration/registration_complete.html'}, name='registrationsuccess'),
)
