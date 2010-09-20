from django.conf.urls.defaults import *


urlpatterns = patterns('hacklab.biblioteka.views',
    (r'^/$', 'index'),
	(r'^/kniga/(?P<k_id>\d+)/$', 'view_kniga'),
	(r'^/godina/(?P<godina>\d+)/$', 'by_godina'),
	(r'^/tag/(?P<tag>\w+)/$', 'by_tag'),
	(r'^/avtor/(?P<a_id>\d+)/$', 'by_author'),
)