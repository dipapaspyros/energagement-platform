from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

import views
from designer import api

urlpatterns = patterns('',
                       # main views
                       url(r'^overview/$', views.overview, name='designer-overview'),
                       url('^(?P<pk>\d+)/details/$', views.details, name='designer-unit-details'),

                       # forms
                       url(r'^unit-create/(?P<unit_type>.*)/$', views.unit_create_form, name='unit-create-form'),

                       # api
                       # nothing yet
                       )
