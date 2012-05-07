from django.conf import settings
from django.http import HttpResponseForbidden

class BlockedIpMiddleware(object):
    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in settings.BLOCKED_IPS:
            return HttpResponseForbidden('<h1>Forbidden</h1>')
        return None
