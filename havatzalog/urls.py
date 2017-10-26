from django.conf.urls import include, url
from django.contrib import admin
from . import views
from panel.views import pupil_create
from accounts.views import login_view, logout_view, register_view


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^panel/', include('panel.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^login/', login_view, name="login"),
    url(r'^register/', register_view, name="register"),
    url(r'^logout/', logout_view, name="logout"),
    url(r'^add-pupil/$', pupil_create, name="pupil-add"),
    # url(r'^export/$', export, name="export"),
]

