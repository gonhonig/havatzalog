from django.conf.urls import url
from . import views

app_name = 'export'

urlpatterns = [
    url(r'^$', views.export, name="export"),
]