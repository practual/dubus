from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^route/(?P<route_num>\w+)/$', views.route),
    url(r'^route/(?P<route_num>\w+)/(?P<direction>outbound|inbound)/$', views.route_stops),
    url(r'^stop/(?P<stop_num>\d+)/$', views.stop),
]
