from django.conf.urls.defaults import *


urlpatterns = patterns('hacklab.biblioteka.views',
    (r'^/$', 'index'),
	(r'^/kniga/(?P<k_id>\d+)/$', 'view_kniga'),
	(r'^/godina/(?P<godina>\d+)/$', 'by_godina'),
	(r'^/tag/(?P<tag>[a-zA-Z0-9 ]+)/$', 'by_tag'),
	(r'^/avtor/(?P<a_id>\d+)/$', 'by_author'),
	(r'^/izdavac/(?P<p_id>\d+)/$', 'by_publisher'),
	(r'^/iznajmi/(?P<k_id>\d+)/$', 'iznajmi'),
	(r'^/iznajmeni_knigi/$', 'iznajmeni'),
	(r'^/rezervirani_knigi/$', 'rezervirani'),
	(r'^/vrati/(?P<k_id>\d+)/$', 'vrati'),
	(r'^/cart/$', 'cart'),
	(r'^/rezerviraj/$', 'rezerviraj'),
	(r'^/cart/remove/$', 'remove_from_cart'),
)