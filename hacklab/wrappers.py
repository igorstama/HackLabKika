from django.template import loader, RequestContext
from django.http import HttpResponse


# Instead of writing "render_to_response('template', {}, context_instance=RequestContext(request))"
# we use this wrapper to save us some time.

def render_to_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return HttpResponse(loader.render_to_string(*args, **kwargs))
