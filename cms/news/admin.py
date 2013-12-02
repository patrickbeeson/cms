from cms.news.models import Story
from django.contrib import admin
from cms.related_links.admin import RelatedLinkInline

class StoryAdmin(admin.ModelAdmin):
	search_fields = ('headline', 'summary', 'tags')
	list_filter = ('pub_date', 'author')
	prepopulated_fields = {"slug": ("headline",)}
	list_display = ('headline', 'pub_date', 'author', 'status')
	ordering = ['-pub_date']
	actions = ['make_published']
	raw_id_fields = ('related_videos','related_audio','related_galleries','related_events','related_publications', 'related_photos', 'photo', 'tease_photo')
	inlines = [
		RelatedLinkInline,
	]

	fieldsets = (
		(None, {
			'fields': ('headline', 'slug', 'subhead', 'dateline', 'summary', 'body', 'tease_photo', 'photo', 'pub_date', 'updated', 'faculty_profiled', 'author', 'one_off_byline', 'media_contact', 'one_off_media_contact')
		}),
		('Categorization', {
			'fields': ('categories', 'tags',)
		}),
		('Related content', {
			'fields': ('related_videos', 'related_audio', 'related_galleries', 'related_events', 'related_publications', 'related_photos', 'related_documents')
		}),
		('Settings', {
			'fields': ('status', 'sites')
		}),
	)
	
	def make_published(self, request, queryset):
		rows_updated = queryset.update(status=1)
		if rows_updated == 1:
			message_bit = "1 story was"
		else:
			message_bit = "%s stories were" % rows_updated
		self.message_user(request, "%s successfully marked as published." % message_bit)

admin.site.register(Story, StoryAdmin)