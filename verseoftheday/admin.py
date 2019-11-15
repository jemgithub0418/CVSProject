from django.contrib import admin

from .models import VerseOfTheDay


class VerseOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'book', 'chapter', 'verse', 'scripture')
    list_display_links = ('day', 'book', 'chapter', 'verse', 'scripture')


admin.site.register(VerseOfTheDay, VerseOfTheDayAdmin)
