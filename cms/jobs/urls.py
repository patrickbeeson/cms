from django.conf.urls.defaults import patterns, include, url
from cms.jobs.models import Job
from django.views.generic import ListView, DetailView

urlpatterns = patterns('',
	(r'^(?P<pk>[-\w]+)/$', DetailView.as_view(
        queryset = Job.objects.all(),
        context_object_name = "job",
        template_name = "jobs/job_detail.html",
    )),

	(r'^$', ListView.as_view(
        queryset = Job.active.all().order_by('-created'),
		context_object_name = "job_list",
		template_name = "jobs/job_list.html",
    )),
)