from django.contrib import admin
from cms.events.models import Event, EventType

class EventTypeAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	
admin.site.register(EventType, EventTypeAdmin)

class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'event_date', 'location', 'speaker', 'status')
	list_filter = ('event_date', 'audience_type', 'status', 'sites', 'event_type')
	search_fields = ('name', 'speaker', 'description', 'tags')
	prepopulated_fields = {'slug': ('name',)}
	actions = ('make_live', 'make_draft')
	raw_id_fields = ['archived_webcast']

	fieldsets = (
		(None, {
			'fields': ('name', 'slug', 'description', 'event_date', 'start_time', 'finish_time', 'is_all_day_event', 'event_type')
		}),
		('Host and speaker', {
			'fields': ('host', 'one_off_host', 'contact_email', 'contact_phone_number', 'speaker', 'speaker_title', 'speaker_bio', 'speaker_website', 'speaker_mugshot')
		}),
		('Attributes', {
			'fields': ('location', 'room_or_area', 'has_webcast', 'archived_webcast', 'notes', 'status', 'lead_image', 'audience_type', 'is_free', 'cost', 'external_URL', 'tags', 'sites')
		}),
	)

	def make_live(self, request, queryset):
		rows_updated = queryset.update(status=3)
		if rows_updated == 1:
			message_bit = "1 event was"
		else:
			message_bit = "%s events were" % rows_updated
		self.message_user(request, "%s successfully marked as live." % message_bit)

	def make_draft(self, request, queryset):
		rows_updated = queryset.update(status=4)
		if rows_updated == 1:
			message_bit = "1 event was"
		else:
			message_bit = "%s events were" % rows_updated
		self.message_user(request, "%s successfully marked as draft." % message_bit)
		
admin.site.register(Event, EventAdmin)