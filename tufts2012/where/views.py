from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.html import escape
import json
from urllib import quote, unquote
from urllib2 import urlopen
from where.forms import LocationForm
from where.models import Location
from util import in_polygon
from random import random
import logging

def home(request):
    return render_to_response('where_home.html', {},
            context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', {},
            context_instance=RequestContext(request))
    
def server_error(request):
    return render_to_response('500.html', {},
            context_instance=RequestContext(request))

def page_not_found(request):
    return render_to_response('404.html', {},
            context_instance=RequestContext(request))

def search_loc_ajax(request):
    address=request.REQUEST.get("location");
    if address is None or len(address) == 0: return HttpResponse({})
    address = address.rstrip().lstrip()
    geocode_url = "%s?address=%s&sensor=false" % (settings.GEOCODING_URL, quote(address))
    json_data = str(urlopen(geocode_url).read())
    obj = json.loads(json_data)
    try:
        lat = obj['results'][0]['geometry']['location']['lat']
        lon = obj['results'][0]['geometry']['location']['lng']
    except IndexError, KeyError:
        return HttpResponse("")
    return HttpResponse(json.dumps(dict(lat=float(lat),lon=float(lon))))

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
    email_subject = "[TUFTS2012] "
    email_body = ""
    email_from = "root@tufts2012.com"
    email_to = [settings.ADMINS[0][1]]
    email_ip = request.META['REMOTE_ADDR']
    form = LocationForm(data=request.POST)
    if not form.is_valid():
        return render_to_response('snippets/location_form.html',
                {'form': form, 'added': False},
                context_instance=RequestContext(request))
    address = form.cleaned_data.get('name')
    fname = form.cleaned_data.get('first_name').rstrip().lstrip().title()
    lname = form.cleaned_data.get('last_name').rstrip().lstrip().title()
    uname = "%s%s" % (fname.lower(), lname.lower())
    if len(uname) > 30:
        uname = uname[0:30]
    geocode_url = "%s?address=%s&sensor=false" % (settings.GEOCODING_URL, quote(address))
    json_data = str(urlopen(geocode_url).read())
    obj = json.loads(json_data)
    try:
        lat = obj['results'][0]['geometry']['location']['lat']
        lon = obj['results'][0]['geometry']['location']['lng']
    except IndexError, KeyError:
        return render_to_response('snippets/location_form.html',
                {'form': form, 'added': False},
                context_instance=RequestContext(request))
    # Randomize location so markers dont overlap
    randomizer = settings.LAT_LONG_RANDOMIZER
    lat = lat + randomizer * random() - randomizer/2
    lon = lon + randomizer * random() - randomizer/2
    try:
        user = User.objects.get(username=uname)
    except User.DoesNotExist:
        user = User.objects.create(first_name=fname, last_name=lname, username=uname)
        email_subject += "Created user %s" % uname
        email_body = "User %s was created by ip %s at location %s" % \
                (user.get_full_name(), email_ip, address)
    try:
        location = user.location.get()
        location.lat = lat
        location.lon = lon
        location.user = user
        email_subject += "Updated user %s" % uname
        email_body = "User %s moved from %s to %s by ip %s." % (user.get_full_name(),
            location.name, address, email_ip)
        location.name = address
        location.save()
    except Location.DoesNotExist:
        location = Location.objects.create(lat=lat, lon=lon, user=user, name=address)
    name = user.get_full_name()
    form = LocationForm()
    if not settings.DEBUG:
        send_mail(email_subject, email_body, email_from, email_to, True)
    return render_to_response('snippets/location_form.html',
            {'form' :form, 'added': True, 'lat': lat, 'lon': lon,
                'name' :name, 'location' :address},
            context_instance=RequestContext(request))

def find_area(request, coords):
    coords = coords.split(",,")
    users = User.objects.all().select_related('location')
    polygon_coords = [coord.split(',') for coord in coords]
    polygon_coords = map(lambda x: [float(x[0]), float(x[1])], polygon_coords)
    selected_users = []
    for user in users:
        try:
            loc = user.location.get()
            lat = float(loc.lat)
            lon = float(loc.lon)
            if in_polygon(lat, lon, polygon_coords):
                selected_users.append(dict(name=escape(user.get_full_name()), id=user.id,
                                           loc=escape(loc.name), lat=lat, lon=lon))
        except Location.DoesNotExist:
            logging.error("ERROR1: User %s has no locations" % user)
        except Location.MultipleObjectsReturned:
            logging.error("ERROR2: User %s has multiple locations" % user)
    return HttpResponse(json.dumps(selected_users))

def search_ajax(request):
    term = request.REQUEST.get('term').rstrip().lstrip().split()
    term1 = term[0]
    try:
        term2 = term[1]
    except IndexError:
        term2 = term1
    locations = Location.objects.filter(Q(user__first_name__icontains=term1) \
            | Q(user__last_name__icontains=term2)).select_related('user')
    matches = []
    for loc in locations:
        label = loc.user.get_full_name()
        value = loc.user.id
        matches.append(dict(label=label, value=value, lat=float(loc.lat),
            lon=float(loc.lon), name=loc.name))
    return HttpResponse(json.dumps(matches))
