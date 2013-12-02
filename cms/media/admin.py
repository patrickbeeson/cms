from cms.media.models import Photo, Video, Audio, Gallery, AudioFile, GalleryPhoto
from django.contrib import admin

class AudioFileInline(admin.StackedInline):
	model = AudioFile
	extra = 1

class AudioAdmin(admin.ModelAdmin):
	search_fields = ('title', 'description', 'tags')
	list_filter = ('uploaded', 'producer', 'status')
	prepopulated_fields = {"slug": ("title",)}
	list_display = ('title', 'status', 'uploaded')
	ordering = ['uploaded']
#	readonly_fields = ('thumbnail_width', 'thumbnail_height')
	inlines = [
		AudioFileInline,
	]

	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'description', 'producer', 'one_off_producer', 'uploaded')
		}),
		('Photo thumbnail', {
			'fields': ('thumbnail', 'thumbnail_alt_text')
		}),
		('Categorization', {
			'fields': ('faculty_profiled', 'category', 'tags',)
		}),
		('Settings', {
			'fields': ('status', 'sites')
		}),
	)

admin.site.register(Audio, AudioAdmin)

class PhotoAdmin(admin.ModelAdmin):
	search_fields = ('title', 'caption', 'tags')
	list_filter = ('uploaded', 'photographer', 'status', 'is_aggregated')
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'uploaded', 'status')
	ordering = ['-uploaded']
	actions = ['make_aggregated']
	readonly_fields = ('width', 'height')

	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'photo', 'caption', 'photographer', 'one_off_photographer', 'uploaded')
		}),
		('Attributes', {
			'fields': ('width', 'height', 'alt_text', 'external_url',)
		}),
		('Categorization', {
			'fields': ('category', 'tags',)
		}),
		('Settings', {
			'fields': ('status', 'sites', 'is_aggregated')
		}),
	)

	def make_aggregated(self, request, queryset):
		rows_updated = queryset.update(is_aggregated=True)
		if rows_updated == 1:
			message_bit = "1 photo was"
		else:
			message_bit = "%s photos were" % rows_updated
		self.message_user(request, "%s successfully marked as aggregated." % message_bit)

admin.site.register(Photo, PhotoAdmin)

class GalleryPhotoInline(admin.StackedInline):
	model = GalleryPhoto
	extra = 3
	raw_id_fields = ['photo']

class GalleryAdmin(admin.ModelAdmin):
	search_fields = ('title', 'description', 'tags')
	list_filter = ('created', 'status')
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'created', 'status')
	ordering = ['created']
	inlines = [
		GalleryPhotoInline,
	]
	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'description', 'created',)
		}),
		('Categorization', {
			'fields': ('category', 'tags',)
		}),
		('Settings', {
			'fields': ('status', 'sites')
		}),
	)

admin.site.register(Gallery, GalleryAdmin)

class VideoAdmin(admin.ModelAdmin):
	search_fields = ('title', 'caption', 'tags')
	list_filter = ('created', 'videographer', 'status', 'is_aggregated')
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'created', 'videographer', 'status', 'is_expired')
	readonly_fields = ('embed_width', 'embed_height')
	actions = ['make_aggregated']
	ordering = ['created']

	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'embed_url', 'caption', 'videographer', 'one_off_videographer', 'created' )
		}),
		('Attributes', {
			'fields': ('external_source', 'embed_width', 'embed_height','external_url','thumbnail', 'thumbnail_alt_text')
		}),
		('Categorization', {
			'fields': ('faculty_profiled', 'category', 'tags')
		}),
		('Settings', {
			'fields': ('is_aggregated', 'expires', 'status', 'sites')
		}),
	)

	def make_aggregated(self, request, queryset):
		rows_updated = queryset.update(is_aggregated=True)
		if rows_updated == 1:
			message_bit = "1 video was"
		else:
			message_bit = "%s videos were" % rows_updated
		self.message_user(request, "%s successfully marked as aggregated." % message_bit)

admin.site.register(Video, VideoAdmin)