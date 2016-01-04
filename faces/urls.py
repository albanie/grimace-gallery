from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'experiments/alexnet-filters$', views.alexnet_filters, name='alexnet-filters'),
        url(r'experiments/$', views.experiments, name='experiments'),
        url(r'progress/$', views.progress, name='progress'),
        url(r'related-work/eigenfaces/$', views.eigenfaces, name='eigenfaces'),
        url(r'related-work/$', views.related_work, name='related-work'),
        url(r'^cyclists/(?P<year>[a-z0-9]+)/(?P<gradient>[a-z]+)/(?P<stage>[a-z0-9]+)/$', 
            views.CyclistGalleryView.as_view(), name='cyclists-year-gradient-stage'),
        url(r'^cyclists/(?P<year>[a-z0-9]+)/(?P<gradient>[a-z]+)/$', views.CyclistGalleryView.as_view(), name='cyclists-year-gradient'),
        url(r'^cyclists/(?P<year>[0-9]+)/$', views.CyclistGalleryView.as_view(), name='cyclists-year'),
        url(r'^cyclists/$', views.CyclistGalleryView.as_view(), name='cyclists-all'),
]

