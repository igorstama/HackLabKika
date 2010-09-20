from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.decorators.csrf import csrf_protect

urlpatterns = patterns('hacklab.registration.views',
	url(r'^/$', login_required(direct_to_template), {'template': 'account/profile.html'}, name="account_profile"),
	(r'^/edit_account/$', 'edit_account'),
	
	url(r'^/login/$', csrf_protect(login), {'template_name': 'account/login.html'}, name="user_login"),
	(r'^/logout/$', logout, {'template_name': 'account/logout.html'}),
	url(r'^/reset_password/$', csrf_protect(password_reset), name="reset_password"),
	url(r'^/reset_password/success/$', password_reset_done, name="reset_password_done"),
	(r'^/reset_password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', csrf_protect(password_reset_confirm), 
		{'template_name':'registration/password_reset_confirm.html'}, 'reset_password_confirm'),
	(r'^/reset_password/complete/$', password_reset_complete),
	url(r'^/change_password/$', login_required(csrf_protect(password_change)), {'template_name':'account/password_change.html'}, name="changepassword"),
	(r'^/change_password/success/$', password_change_done, {'template_name': 'account/password_change_done.html'}),
)
