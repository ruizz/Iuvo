from django.conf.urls import patterns, url
from planner import views

urlpatterns = patterns('',
	# ex: /planner/
	url(r'^$', views.index, name='index'),
	# ex: /planner/user/john.doe/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/account/$', 
		views.userAccountView, name='userAccount'),
	# ex: /planner/user/john.doe/degreeplans/1/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/degreeplans/(?P<dpID>\d+)/$', views.degreePlanView, name='degreePlan'),
)