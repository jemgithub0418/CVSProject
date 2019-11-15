from django.db import models

# Create your models here.
DAY_LEVEL_CHOICES = (('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                     ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),)


class VerseOfTheDay(models.Model):
    day = models.CharField(choices=DAY_LEVEL_CHOICES, unique=True, max_length=12)
    book = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    verse = models.CharField(max_length=100)
    scripture = models.TextField(max_length=None)

    class Meta:
        verbose_name_plural = 'verse of the day'
        ordering = ('day',)

    def __str__(self):
        return f"Verse for {self.day}. ({self.book} {self.chapter}:{self.verse})"
