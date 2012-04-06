from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', 'where.views.home'),
        url(r'^json/$', 'where.views.locations_json'),
        url(r'^where/new/$', 'where.views.location_form'),
        url(r'^where/create/$', 'where.views.add_location'),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'tufts2012.views.home', name='home'),
    # url(r'^tufts2012/', include('tufts2012.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'^admin/', include(admin.site.urls)),
)
