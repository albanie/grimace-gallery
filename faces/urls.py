from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^cyclists/$', views.CyclistGalleryView.as_view(), name='cyclist_index'),
]

