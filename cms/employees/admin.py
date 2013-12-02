from cms.employees.models import Education, Employee, Publication
from django.contrib import admin
from cms.related_links.admin import RelatedLinkInline

class EducationInline(admin.StackedInline):
	model = Education
	extra = 1

class PublicationInline(admin.StackedInline):
	model = Publication
	extra = 1
	prepopulated_fields = {"slug": ("article_title",)}

class PublicationAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("article_title",)}
	search_fields = ('article_title', 'slug', 'authors')
	list_filter = ('publication_type', 'journal_pub_date', 'is_featured')
	list_display = ('article_title', 'primary_author', 'journal_name')
	actions = ['make_featured']

	def make_featured(self, request, queryset):
		rows_updated = queryset.update(is_featured=True)
		if rows_updated == 1:
			message_bit = "1 publication was"
		else:
			message_bit = "%s publications were" % rows_updated
		self.message_user(request, "%s successfully marked as featured." % message_bit)

class EmployeeAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('first_name', 'middle_name', 'last_name')}
	search_fields = ('first_name', 'last_name', 'title')
	list_filter = ('employee_type', 'is_currently_employed')
	list_display = ('first_name', 'last_name', 'slug', 'employee_type', 'title')
	save_on_top = True
	ordering = ['last_name']
	inlines = [
		RelatedLinkInline,
		EducationInline,
		PublicationInline,
	]
	fieldsets = (
		(None, {
			'fields': ('user', 'first_name', 'middle_name', 'last_name', 'slug', 'title', 'photo', 'job_description')
		}),
		('Contact information', {
			'fields': ('office_phone_number', 'mobile_phone_number', 'office', 'email', 'website')
		}),
		('Background information', {
			'fields': ('previous_position', 'lead_image', 'resume_or_cv')
		}),	
		('Settings', {
			'fields': ('employee_type', 'is_currently_employed', 'sites')
		}),
	)

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Employee, EmployeeAdmin)