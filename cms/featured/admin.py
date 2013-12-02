from cms.featured.models import StoryList, FeaturedStory, Poster, PosterItem
from django.contrib import admin

class PosterItemInline(admin.StackedInline):
	model = PosterItem
	extra = 5
	max_num = 5
	raw_id_fields = ['image']
	fieldsets = (
		(None, {
			'fields': ('title', 'tease', 'link', 'image', 'orientation')
		}),
	)

class PosterAdmin(admin.ModelAdmin):
	inlines = [
		PosterItemInline,
	]

	fieldsets = (
		(None, {
			'fields': ('name', 'live_date', 'site')
		}),
	)

class FeaturedStoryInline(admin.StackedInline):
	model = FeaturedStory
	extra = 10
	max_num = 10
	raw_id_fields = ['story']
	fieldsets = (
		(None, {
			'fields': ('story',)
		}),
	)

class StoryListAdmin(admin.ModelAdmin):
	inlines = [
		FeaturedStoryInline,
	]

	fieldsets = (
		(None, {
			'fields': ('name', 'live_date', 'site'), 'description': ('Note: Only stories with tease photos will display a thumbnailed image beside the headline.')
		}),
	)

admin.site.register(Poster, PosterAdmin)
admin.site.register(StoryList, StoryListAdmin)
