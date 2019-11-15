from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings


class YearLevel(models.Model):
    year = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.year

    def save(self, *args, **kwargs):
        for field_name in ['year']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(YearLevel, self).save(*args, **kwargs)


class Section(models.Model):
    section = models.CharField(max_length=100)
    year_level = models.ForeignKey(YearLevel, on_delete=models.SET_NULL, null=True)
    # class_advisor = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to=Q(
    #     is_teacher=True), related_name='class_advisor')
    # students_enrolled = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL, limit_choices_to=Q(is_student=True), related_name='students_enrolled')

    def __str__(self):
        return self.section


class Subject(models.Model):
    subject_name = models.CharField(max_length=150)
    subject_code = models.CharField(max_length=50)
    year = models.ForeignKey(YearLevel, null=True, on_delete=models.SET_NULL)
    units = models.CharField(max_length=10)

    def __str__(self):
        return self.subject_name + ' ' + '(' + self.subject_code + ')'


class StudentGrade(models.Model):
    PERIOD_CHOICES = [
        ('First Grading', 'First Grading'),
        ('Second Grading', 'Second Grading'),
        ('Third Grading', 'Third Grading'),
        ('Fourth Grading', 'Fourth Grading'),
        ('First Semester', 'First Semester'),
        ('Second Semester', 'Second Semester')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, limit_choices_to=Q(is_student=True))
    period = models.CharField(choices=PERIOD_CHOICES, max_length=25)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True,)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
