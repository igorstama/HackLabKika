from django.conf.urls.defaults import *
from hacklab.biblioteka.views import return_book, reserve_book
from django.views.decorators.csrf import csrf_protect

urlpatterns = patterns('hacklab.biblioteka.views',
    (r'^/$', 'index'),
	(r'^/book/(?P<k_id>\d+)/$', 'view_book_details'),
	(r'^/year/(?P<godina>\d+)/$', 'by_year'),
	(r'^/tag/(?P<tag>[a-zA-Z0-9 ]+)/$', 'by_tag'),
	(r'^/author/(?P<a_id>\d+)/$', 'by_author'),
	(r'^/publisher/(?P<p_id>\d+)/$', 'by_publisher'),
	(r'^/iznajmi/(?P<k_id>\d+)/$', 'rent_book'),
	(r'^/rented_books/$', 'history'),
	(r'^/rented_books/(?P<year>[0-9]{4})/$', 'history'),
	(r'^/rented_books/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'history'),
	(r'^/history/$', 'my_history'),
	(r'^/history/(?P<year>[0-9]{4})/$', 'my_history'),
	(r'^/history/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'my_history'),
	(r'^/return_book/(?P<k_id>\d+)/$', 'return_book'),
	(r'^/reservations/$', 'reserved_books'),
	(r'^/reservations/make/$', 'reserve_book'),
	(r'^/reservations/remove/$', 'remove_reservation'),
)

