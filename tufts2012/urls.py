from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', 'where.views.home'),
        url(r'^json/$', 'where.views.locations_json'),
        url(r'^about/$', 'where.views.about'),
        url(r'^where/new/$', 'where.views.location_form'),
        url(r'^where/create/$', 'where.views.add_location'),
        url(r'^where/filter/$', 'where.views.search_ajax'),
        url(r'^where/searchloc/$', 'where.views.search_loc_ajax'),
        url(r'^where/area/$', 'where.views.find_area'),
        url(r'^where/area/(?P<coords>[\d,-\.\+]+)/$', 'where.views.find_area'),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT}),
      url(r'^admin/', include(admin.site.urls)),
)
