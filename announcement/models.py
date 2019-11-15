from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)

    REQUIRED_FIELDS = ['title', 'content', ]

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
