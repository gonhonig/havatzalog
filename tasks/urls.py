from django.conf.urls import url
from . import views

app_name = 'tasks'

urlpatterns = [
    url(r'^$', views.tasks, name="tasks"),
    url(r'^(?P<task_id>[0-9]+)/done$', views.done, name="done"),
    url(r'^(?P<task_id>[0-9]+)/undone$', views.undone, name="undone"),
]
