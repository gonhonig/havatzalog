from django.conf.urls import url
from . import views

app_name = 'panel'

urlpatterns = [
    url(r'^$', views.selector, name="selector"),
    url(r'^(?P<pupil_id>[0-9]+)/$', views.pupil, name="pupil"),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.ChangePermissions.as_view(), name="change-permissions"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/$', views.parameter, name="parameter"),
    url(r'^(?P<pupil_id>[0-9]+)/add/$', views.cut_create, name="cut-add"),
    url(r'^(?P<pupil_id>[0-9]+)/add-event/$', views.event_create, name="event-add"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/(?P<cut_id>[0-9]+)/$', views.cut_delete, name="cut-delete"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/add/$', views.cut_create_specific, name="cut-add-specific"),
    url(r'^(?P<pupil_id>[0-9]+)/add/parameter-add/$', views.parameter_create, name="parameter-add"),
]
