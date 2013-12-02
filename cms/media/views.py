from django.views.generic import DateDetailView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from cms.media.models import Gallery, Photo, Audio, Video

class GalleryDetailView(DateDetailView):

	date_field = "created"
	template_name = "media/gallery_detail.html"
	context_object_name = "gallery"
	slug_field = "slug"

	def get_queryset(self):
		galleries = None
		if self.request.user.is_staff:
			galleries = Gallery.objects.all()
		else:
			galleries = Gallery.live.all()
		return galleries

class PhotoDetailView(DateDetailView):

	date_field = "uploaded"
	template_name = "media/photo_detail.html"
	context_object_name = "photo"
	slug_field = "slug"

	def get_queryset(self):
		photos = None
		if self.request.user.is_staff:
			photos = Photo.objects.all()
		else:
			photos = Photo.live.all()
		return photos


class AudioDetailView(DetailView):

	date_field = "uploaded"
	template_name = "media/audio_detail.html"
	context_object_name = "audio"
	slug_field = "slug"

	def get_queryset(self):
		audio = None
		if self.request.user.is_staff:
			audio = Audio.objects.all()
		else:
			audio = Audio.live.all()
		return audio
		
class VideoDetailView(DateDetailView):

	date_field = "created"
	template_name = "media/video_detail.html"
	context_object_name = "video"
	slug_field = "slug"

	def get_queryset(self):
		videos = None
		if self.request.user.is_staff:
			videos = Video.objects.all()
		else:
			videos = Video.live.all()
		return videos