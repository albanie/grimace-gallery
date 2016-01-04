from random import shuffle
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .models import Face
from .dataset_graphs import get_data_chart, get_binary_classification_chart
from .dataset_graphs import get_binary_class_boundary 
from .experiment_graphs import get_data_partition_chart
from .experiment_graphs import get_alexnet_binary_training_fig
from .experiment_graphs import get_alexnet_binary_testing_fig
from .experiment_graphs import get_alexnet_binary_ROC_fig
from .experiment_graphs import find_best_epoch, get_alexnet_data

def index(request):
    template = loader.get_template('faces/index.html')
    faces = get_num_faces(min_size=settings.MIN_FACE_SIZE)
    num_total_faces = (faces['2012']['num_faces'] +
                       faces['2013']['num_faces'] + 
                       faces['2014']['num_faces'] +
                       faces['2015']['num_faces'])
    data_chart = get_data_chart()
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
        'num_faces_2015': faces['2015']['num_faces'],
        'min_gradient_2015': faces['2015']['min_gradient'],
        'max_gradient_2015': faces['2015']['max_gradient'],
        'chart': data_chart,
        })
    return HttpResponse(template.render(context))

def experiments(request):
    template = loader.get_template('faces/experiments.html')
    binary_class_boundary = get_binary_class_boundary()
    data_partition_chart = get_data_partition_chart()
    chart = get_binary_classification_chart()
    alexnet_binary_training_chart = get_alexnet_binary_training_fig()
    alexnet_binary_testing_chart = get_alexnet_binary_testing_fig()
    alexnet_binary_ROC_chart = get_alexnet_binary_ROC_fig()
    train, val = get_alexnet_data()
    best_epoch = find_best_epoch(val)
    context = RequestContext(request, {
        'data_partition_chart': data_partition_chart,
        'binary_classification_chart': chart,
        'binary_class_boundary': round(binary_class_boundary, 2),
        'alexnet_binary_training_chart': alexnet_binary_training_chart,
        'alexnet_binary_testing_chart': alexnet_binary_testing_chart,
        'alexnet_binary_ROC_chart': alexnet_binary_ROC_chart,
        'best_epoch': best_epoch,
        })
    return HttpResponse(template.render(context))

def related_work(request):
    template = loader.get_template('faces/related_work.html')
    binary_class_boundary = get_binary_class_boundary()
    chart = get_binary_classification_chart()
    context = RequestContext(request, {
        })
    return HttpResponse(template.render(context))

def eigenfaces(request):
    template = loader.get_template('faces/eigenfaces.html')
    context = RequestContext(request, {
        })
    return HttpResponse(template.render(context))

def alexnet_filters(request):
    template = loader.get_template('faces/alexnet_filters.html')
    context = RequestContext(request, {
        })
    return HttpResponse(template.render(context))

def progress(request):
    template = loader.get_template('faces/progress.html')
    context = RequestContext(request, {
        })
    return HttpResponse(template.render(context))

class CyclistGalleryView(generic.ListView):
    template_name = 'faces/cyclist_gallery.html'
    context_object_name = 'face_list'
    year = 'all'
    stage = 'all'
    gradient = 'random'
    paginate_by = 300

    def get_queryset(self, *args, **kwargs):
        """Return filtered subset of faces."""
        year = self.parse_year(self.kwargs)
        gradient = self.parse_gradient(self.kwargs)
        stage = self.parse_stage(self.kwargs)

        faces = self.get_filtered_faces(year, gradient, stage)

        if 'gradient' not in self.kwargs.keys() or self.kwargs['gradient'] == 'random':
            shuffle(faces)
        return faces

    def parse_year(self, url_kwargs):
        """returns the year parsed from the URL as a keyword
        argument."""
        if 'year' not in url_kwargs.keys() or url_kwargs['year'] == 'all':
            year = 'all'
        else:
            year = int(url_kwargs['year'])

        # set updated year attribute on class for return context
        self.year = year
        return year

    def parse_gradient(self, url_kwargs):
        """returns the gradient parsed from the URL as a keyword
        argument, converted into the appropriate queryset filter."""
        if 'gradient' not in url_kwargs.keys() or url_kwargs['gradient'] == 'random':
            self.gradient = 'random'
            gradient_filter = '?'
        elif url_kwargs['gradient'] == 'ascend':
            self.gradient = 'ascend'
            gradient_filter = 'gradient'
        else: # CASE: url_kwargs['gradient'] == 'descend'
            gradient_filter = '-gradient'
            self.gradient = 'descend'

        return gradient_filter
    
    def parse_stage(self, url_kwargs):
        """returns the stage parsed from the URL as a keyword
        argument."""
        if 'stage' not in url_kwargs.keys() or url_kwargs['stage'] == 'all':
            stage = 'all'
        else:
            stage = int(url_kwargs['stage'])

        # set updated year attribute on class for return context
        self.stage = stage
        return stage

    def get_filtered_faces(self, year, gradient, stage):
        """returns filtered queryset containing faces with the given
        year, gradient and stage."""

        if year == 'all':
            if stage == 'all':
                faces = list(Face.objects
                        .filter(size__gte=settings.MIN_FACE_SIZE)
                        .order_by(gradient))
            else: # a specific stage has been given
                faces = list(Face.objects
                        .filter(stage_num=stage, size__gte=settings.MIN_FACE_SIZE)
                        .order_by(gradient))
        else: # a specific year has been given
            if stage == 'all':
                faces = list(Face.objects
                        .filter(year=year, size__gte=settings.MIN_FACE_SIZE)
                        .order_by(gradient))
            else: # a specific stage has also been given
                faces = list(Face.objects
                        .filter(year=year, stage_num=stage, size__gte=settings.MIN_FACE_SIZE)
                        .order_by(gradient))
        return faces

    def get_context_data(self, **kwargs):
        context = super(CyclistGalleryView, self).get_context_data(**kwargs)
        context['year'] = self.year
        context['gradient'] = self.gradient
        context['stage'] = self.stage
        return context

def get_num_faces(min_size):
    """returns the total number of faces with the 
    specified minimum size."""
    faces_in_2012 = list(Face.objects.filter(year=2012, size__gte=min_size).order_by('gradient'))
    faces_in_2013 = list(Face.objects.filter(year=2013, size__gte=min_size).order_by('gradient'))
    faces_in_2014 = list(Face.objects.filter(year=2014, size__gte=min_size).order_by('gradient'))
    faces_in_2015 = list(Face.objects.filter(year=2015, size__gte=min_size).order_by('gradient'))
    
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
            '2015': {'num_faces': len(faces_in_2015),
                     'max_gradient': faces_in_2015[-1].gradient,
                     'min_gradient': faces_in_2015[0].gradient},
                     }
    return num_faces
 


