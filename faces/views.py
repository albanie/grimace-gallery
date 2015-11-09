from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Face

class IndexView(generic.ListView):
    template_name = 'faces/index.html'
    context_object_name = 'face_list'

    def get_queryset(self):
        """Return the first five faces."""
        return Face.objects.order_by('-gradient')

