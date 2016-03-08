from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

import views
from designer import api

urlpatterns = patterns('',
                       # views
                       url(r'^overview/$', views.overview, name='designer-overview'),
                       url('^(?P<pk>\d+)/details/$', views.details, name='designer-unit-details'),

                       # api
                       # nothing yet
                       )
