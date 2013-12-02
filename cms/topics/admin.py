from django.contrib import admin
from cms.topics.models import Topic

class TopicAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'is_expired')
	prepopulated_fields = {'slug': ('title',)}

	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'description', 'is_expired', 'sites')
		}),
		('Content for topic', {
			'fields': ('stories', 'photos', 'videos', 'audio', 'galleries', 'documents', 'faculty')
		}),
	)
	
admin.site.register(Topic, TopicAdmin)