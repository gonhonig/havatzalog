from django.conf.urls import url
from . import views

app_name = 'panel'

urlpatterns = [
    url(r'^$', views.selector, name="selector"),
    url(r'^(?P<pupil_id>[0-9]+)/$', views.pupil, name="pupil"),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.ChangePermissions.as_view(), name="change-permissions"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/$', views.parameter, name="parameter"),
    url(r'^(?P<pupil_id>[0-9]+)/add/$', views.cut_create, name="cut-add"),
    url(r'^(?P<pupil_id>[0-9]+)/events/$', views.events, name="events"),
    url(r'^(?P<pupil_id>[0-9]+)/add-event/$', views.event_create, name="event-add"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/$', views.event, name="event"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/edit/$', views.event_edit, name="event-edit"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/delete/$', views.event_delete, name="event-delete"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/(?P<cut_id>[0-9]+)/del/$', views.cut_delete, name="cut-delete"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/(?P<cut_id>[0-9]+)/del/$', views.cut_delete2, name="cut-delete2"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/(?P<cut_id>[0-9]+)/edit/$', views.cut_edit, name="cut-edit"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/(?P<cut_id>[0-9]+)/edit/$', views.cut_edit2, name="cut-edit2"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/add/$', views.cut_create_specific, name="cut-add-specific"),
    url(r'^(?P<pupil_id>[0-9]+)/add/parameter-add/$', views.parameter_create, name="parameter-add"),
    url(r'^(?P<pupil_id>[0-9]+)/add-event/parameter-add/$', views.parameter_create_from_event, name="parameter-add-from-event"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/edit/parameter-add/$', views.parameter_create_from_event_edit, name="parameter-add-from-event-edit"),
    url(r'^(?P<pupil_id>[0-9]+)/(?P<parameter_id>[0-9]+)/(?P<cut_id>[0-9]+)/edit/parameter-add/$', views.parameter_create_from_cut_edit, name="parameter-add-from-cut-edit"),
    url(r'^(?P<pupil_id>[0-9]+)/events/(?P<event_id>[0-9]+)/(?P<cut_id>[0-9]+)/edit/parameter-add/$', views.parameter_create_from_cut_edit2, name="parameter-add-from-cut-edit2"),
]
