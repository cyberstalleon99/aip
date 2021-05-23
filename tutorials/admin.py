from django.contrib import admin
from .models import Tutorial

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    model = Tutorial
    list_display = ['title', 'video_link', 'slug', 'search_keywords']
    exclude = ['slug']

    def search_keywords(self, video):
        return video.tags_str()

