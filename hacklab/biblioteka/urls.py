from django.conf.urls.defaults import *
from hacklab.biblioteka.views import return_book, reserve_book
from django.views.decorators.csrf import csrf_protect

urlpatterns = patterns('hacklab.biblioteka.views',
    (r'^/$', 'index'),
	(r'^/kniga/(?P<k_id>\d+)/$', 'view_book_details'),
	(r'^/godina/(?P<godina>\d+)/$', 'by_year'),
	(r'^/tag/(?P<tag>[a-zA-Z0-9 ]+)/$', 'by_tag'),
	(r'^/avtor/(?P<a_id>\d+)/$', 'by_author'),
	(r'^/izdavac/(?P<p_id>\d+)/$', 'by_publisher'),
	(r'^/iznajmi/(?P<k_id>\d+)/$', 'rent_book'),
	(r'^/iznajmeni_knigi/$', 'history'),
	(r'^/iznajmeni_knigi/(?P<year>[0-9]{4})/$', 'history'),
	(r'^/iznajmeni_knigi/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'history'),
	(r'^/rezervirani_knigi/$', 'reserved_books'),
	(r'^/istorija/$', 'my_history'),
	(r'^/istorija/(?P<year>[0-9]{4})/$', 'my_history'),
	(r'^/istorija/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'my_history'),
	(r'^/vrati/(?P<k_id>\d+)/$', 'return_book'),
	(r'^/cart/$', 'cart'),
	(r'^/rezerviraj/$', 'reserve_book'),
	(r'^/cart/remove/$', 'remove_from_cart'),
)

