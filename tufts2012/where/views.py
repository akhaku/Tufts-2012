from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from urllib import quote
from urllib2 import urlopen
from where.forms import LocationForm
from where.models import Location
import logging

def home(request):
    return render_to_response('where_home.html', {},
            context_instance=RequestContext(request))

def locations_json(request):
    locations = Location.objects.all().select_related('user');
    return render_to_response('locations_json.json',{'locations': locations},
            context_instance=RequestContext(request))
 
def location_form(request):
    form = LocationForm
    return render_to_response('snippets/location_form.html',
            {'form': form, 'added': False},
            context_instance=RequestContext(request))

def add_location(request):
    name = "Bob Dylan"
    address = quote(request.REQUEST.get('name'))
    geocode_url = "%s?address=%s&sensor=false" % (settings.GEOCODING_URL, address)
    json_data = str(urlopen(geocode_url).read())
    obj = json.loads(json_data) # TODO catch IndexError, KeyError parse error etc
    lat = obj['results'][0]['geometry']['location']['lat']
    lon = obj['results'][0]['geometry']['location']['lng']
    location = request.REQUEST.get('name')
    form = LocationForm()
    return render_to_response('snippets/location_form.html',
            {'form' :form, 'added': True, 'lat': lat, 'lon': lon,
                'name' :name, 'location' :location},
            context_instance=RequestContext(request))

