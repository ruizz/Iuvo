from django.conf.urls import patterns, url
from planner import views

urlpatterns = patterns('',
	# ex: /planner/
	url(r'^$', views.index, name='index'),
	# ex: /planner/u/john.doe/
	url(r'^u/(?P<username>[A-Za-z0-9.-_]+)/$', views.userAccountPage, name='userAccountPage')
)