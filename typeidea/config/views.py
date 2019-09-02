from django.http import HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMixin
from config.models import Link

#
# def links(request):
#     return HttpResponse('links')


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    context_object_name = 'link_list'
    template_name = 'config/links.html'
