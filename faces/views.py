from random import shuffle
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .models import Face
from .graph import get_chart

def index(request):
    template = loader.get_template('faces/index.html')
    faces = get_num_faces(min_size=settings.MIN_FACE_SIZE)
    num_total_faces = (faces['2012']['num_faces'] +
                       faces['2013']['num_faces'] + 
                       faces['2014']['num_faces'])
    chart = get_chart()
    context = RequestContext(request, {
        'num_total_faces': num_total_faces,
        'min_face_size': settings.MIN_FACE_SIZE,
        'num_faces_2012': faces['2012']['num_faces'],
        'min_gradient_2012': faces['2012']['min_gradient'],
        'max_gradient_2012': faces['2012']['max_gradient'],
        'num_faces_2013': faces['2013']['num_faces'],
        'min_gradient_2013': faces['2013']['min_gradient'],
        'max_gradient_2013': faces['2013']['max_gradient'],
        'num_faces_2014': faces['2014']['num_faces'],
        'min_gradient_2014': faces['2014']['min_gradient'],
        'max_gradient_2014': faces['2014']['max_gradient'],
        'chart': chart,
        })
    return HttpResponse(template.render(context))

class CyclistGalleryView(generic.ListView):
    template_name = 'faces/cyclist_gallery.html'
    context_object_name = 'face_list'

    def get_queryset(self):
        """Return subset of faces."""
        all_faces = list(Face.objects.filter(size__gte=settings.MIN_FACE_SIZE).order_by('-gradient'))
        shuffle(all_faces)
        return all_faces[:500]

def get_num_faces(min_size):
    """returns the total number of faces with the 
    specified minimum size."""
    faces_in_2012 = list(Face.objects.filter(year=2012, size__gte=min_size).order_by('gradient'))
    faces_in_2013 = list(Face.objects.filter(year=2013, size__gte=min_size).order_by('gradient'))
    faces_in_2014 = list(Face.objects.filter(year=2014, size__gte=min_size).order_by('gradient'))
    
    num_faces = {
            '2012': {'num_faces': len(faces_in_2012),
                     'max_gradient': faces_in_2012[-1].gradient,
                     'min_gradient': faces_in_2012[0].gradient},
            '2013': {'num_faces': len(faces_in_2013),
                     'max_gradient': faces_in_2013[-1].gradient,
                     'min_gradient': faces_in_2013[0].gradient},
            '2014': {'num_faces': len(faces_in_2014),
                     'max_gradient': faces_in_2014[-1].gradient,
                     'min_gradient': faces_in_2014[0].gradient},
                     }
    return num_faces
 


