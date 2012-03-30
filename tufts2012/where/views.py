from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from where.models import Location

def home(request):
    return render_to_response('where_home.html', {},
            context_instance=RequestContext(request))

def locations_json(request):
    locations = Location.objects.all().select_related('user');
    return render_to_response('locations_json.json',{'locations': locations},
            context_instance=RequestContext(request))
