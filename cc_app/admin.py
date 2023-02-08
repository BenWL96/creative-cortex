from django.contrib import admin
from . import models
admin.site.register(models.Images)
admin.site.register(models.Pages)
admin.site.register(models.Personnel)
admin.site.register(models.Comic_Personnel)
admin.site.register(models.Landing_Page_Images)
admin.site.register(models.Gallery_images)
admin.site.register(models.Web_Pages)
admin.site.register(models.Web_Page_Text_Content)
admin.site.register(models.Featured_Youtube_videos)
admin.site.register(models.Inquiries)


class ComicsAdmin(admin.ModelAdmin):
	exclude = ('slug',)

class VolumesAdmin(admin.ModelAdmin):
	exclude = ('slug_volume_title',)
class ChaptersAdmin(admin.ModelAdmin):
	exclude = ('slug_chapter_title',)

admin.site.register(models.Comics, ComicsAdmin)
admin.site.register(models.Volumes, VolumesAdmin)
admin.site.register(models.Chapters, ChaptersAdmin)