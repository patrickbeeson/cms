from cms.jobs.models import Job
from django.contrib import admin

def make_expired(modeladmin, request, queryset):
    queryset.update(is_expired=True)
make_expired.short_description = "Mark selected jobs as expired"

class JobAdmin(admin.ModelAdmin):
	search_fields = ('title', 'posting_number', 'description')
	list_filter = ('created', 'is_expired')
	list_display = ('title', 'slug', 'posting_number', 'posting_end_date', 'is_expired')
	ordering = ['title']
	prepopulated_fields = {"slug": ("title",)}
	actions = [make_expired]

admin.site.register(Job, JobAdmin)