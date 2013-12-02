from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from cms.employees.models import Employee, Publication
from cms.press.models import Mention

class EmployeePublicationsListView(ListView):

    context_object_name = "publication_list"
    template_name = "employees/publications_by_employee.html"
    paginate_by = 50

    def get_queryset(self):
        self.primary_author = get_object_or_404(Employee, slug__iexact=self.kwargs['slug'])
        return Publication.objects.filter(primary_author=self.primary_author)

    def get_context_data(self, **kwargs):
        context = super(EmployeePublicationsListView, self).get_context_data(**kwargs)
        context['primary_author'] = self.primary_author
        return context

class EmployeePressListView(ListView):

    context_object_name = "mention_list"
    template_name = "employees/press_by_employee.html"
    paginate_by = 15

    def get_queryset(self):
        self.faculty_mentioned = get_object_or_404(Employee, slug__iexact=self.kwargs['slug'])
        return Mention.objects.filter(faculty_mentioned=self.faculty_mentioned)

    def get_context_data(self, **kwargs):
        context = super(EmployeePressListView, self).get_context_data(**kwargs)
        context['faculty_mentioned'] = self.faculty_mentioned
        return context

class EmployeeDetailView(DetailView):

	context_object_name = "employee"
	template_name = "employees/employee_detail.html"
	model = Employee
	slug_field = "slug"

	def get_context_data(self, **kwargs):
		context = super(EmployeeDetailView, self).get_context_data(**kwargs)
		context['featuredpublication_list'] = Publication.featured.all().filter(primary_author__slug__iexact=self.kwargs['slug'])[:5]
		return context