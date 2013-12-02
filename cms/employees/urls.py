from django.conf.urls.defaults import patterns, include, url
from cms.employees.models import Employee
from django.views.generic import ListView, DetailView
from cms.employees.views import EmployeePublicationsListView, EmployeePressListView, EmployeeDetailView

urlpatterns = patterns('',
    (r'^$', ListView.as_view(
    	context_object_name = "employee_list",
    	template_name = "employees/employee_list.html",
    	queryset = Employee.employed.all(),
    )),
    
    (r'^faculty/$', ListView.as_view(
    	context_object_name = "employee_list",
    	template_name = "employees/faculty_list.html",
    	queryset = Employee.employed.all().filter(employee_type=1),
    )),
    (r'^administrative-support/$', ListView.as_view(
    	context_object_name = "employee_list",
    	template_name = "employees/administrative-support_list.html",
    	queryset = Employee.employed.all().filter(employee_type=2),
    )),
    (r'^research-support/$', ListView.as_view(
    	context_object_name = "employee_list",
    	template_name = "employees/research-support_list.html",
    	queryset = Employee.employed.all().filter(employee_type=3),
    )),
    (r'^postdocs/$', ListView.as_view(
    	context_object_name = "employee_list",
    	template_name = "employees/postdocs_list.html",
    	queryset = Employee.employed.all().filter(employee_type=4),
    )),
	(r'^(?P<slug>[-\w]+)/$', EmployeeDetailView.as_view()),
	
	(r'^(?P<slug>[-\w]+)/publications/$', EmployeePublicationsListView.as_view()),
	
	(r'^(?P<slug>[-\w]+)/press/$', EmployeePressListView.as_view()),
)