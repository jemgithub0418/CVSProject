from django.contrib import admin
from .models import (YearLevel, Section, Subject, StudentGrade)
from accounts.models import User


class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'subject', 'grade')
    list_display_links = ('user', 'period', 'subject', 'grade')
    list_filter = [
        'period',
    ]
    search_fields = [
        'user__first_name', 'user__last_name',
    ]


admin.site.register(YearLevel)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(StudentGrade, StudentGradeAdmin)
