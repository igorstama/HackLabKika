from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = patterns('hacklab.registration.views',
	(r'^/$', login_required(direct_to_template), {'template': 'account/profile.html'}),
	(r'^/edit_account/$', 'edit_account'),
	(r'^/login/$', login, {'template_name': 'account/login.html'}),
	(r'^/logout/$', logout, {'template_name': 'account/logout.html'}),
	(r'^/reset_password/$', password_reset),
	(r'^/reset_password/success/$', password_reset_done),
	(r'^/reset_password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name':'registration/password_reset_confirm.html'}),
	(r'^/reset_password/complete/$', password_reset_complete),
	(r'^/change_password/$', login_required(password_change), {'template_name':'account/password_change.html'}),
	(r'^/change_password/success/$', password_change_done, {'template_name': 'account/password_change_done.html'}),
)