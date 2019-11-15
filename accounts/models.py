from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, pre_save, pre_delete
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import PermissionDenied
# from auditlog.registry import auditlog
from django.db.models import Q
from student_dashboard.models import YearLevel, Section


class User(AbstractUser):
    USER_LEVEL_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('registrar', 'Registrar'),
        ('cm', 'Content Moderator'),
    ]
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    middle_name = models.CharField(max_length=70, blank=True)
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email Address',
        blank=True,
        null=True,
    )
    user_level = models.CharField(_('User Level'), max_length=15,
                                  choices=USER_LEVEL_CHOICES,)

    is_student = models.BooleanField(default=False, verbose_name='Student')
    is_superuser = models.BooleanField(default=False, verbose_name='Administrator')
    is_teacher = models.BooleanField(default=False, verbose_name='Teacher')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_registrar = models.BooleanField(default=False, verbose_name='Registrar')
    is_content_moderator = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        full_name = self.get_full_name()
        return full_name.strip()

    #
    # def __repr__(self):
    #     return gettext(self.first_name + ' '+self.last_name)

    # code below is from: https://stackoverflow.com/questions/17257031/django-unique-null-and-blank-charfield-giving-already-exists-error-on-admin-p

    def save(self, *args, **kwargs):
        # Empty strings are not unique, but we can save multiple NULLs
        if not self.email:
            self.email = None

        for field_name in ['first_name', 'last_name', 'middle_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super().save(*args, **kwargs)  # Python3-style super()


# auditlog.register(User)


class StaffProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to=Q(is_staff=True), related_name='user_staffprofile'
                                )
    employee_number = models.CharField(max_length=20, null=True)
    mobile_number = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


# auditlog.register(StaffProfile)

    # USER_LEVEL_CHOICES = [
    #     ('student', 'Student'),
    #     ('admin', 'Administrator'),
    #     ('teacher', 'Teacher'),
    #     ('registrar', 'Registrar'),
    #     ('cm', 'Content Moderator'),
    # ]
@receiver(pre_save, sender=User)
def check_user_level(sender, instance, *args, **kwargs):
    if not instance.is_student:
        instance.is_staff = True
        if instance.is_superuser:
            instance.user_level = 'admin'
        elif instance.is_teacher:
            instance.user_level = 'teacher'
        elif instance.is_registrar:
            instance.user_level = 'registrar'
        elif instance.is_content_moderator:
            instance.user_level = 'cm'
    else:
        instance.user_level = 'student'

    # if not instance.user_level == 'student':
    #     instance.is_staff = True
    # if instance.user_level == 'cm':
    #     pass
    # if instance.user_level == 'admin':
    #     instance.is_superuser = True
    # if instance.user_level == 'student':
    #     instance.is_student = True
    # if instance.user_level == 'teacher':
    #     instance.is_teacher = True
    # if instance.user_level == 'registrar':
    #     instance.is_registrar = True


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser == True:
        raise PermissionDenied("Administrator accounts cannot be deleted.")
#
# class Student(models.Model):
#     YEAR_LEVEL_CHOICES = ((1, 'Grade1'), (2, 'Grade2'), (3, 'Grade3'),
#                           (4, 'Grade4'), (5, 'Grade5'), (6, 'Grade6'), (7, 'Grade7'), (8, 'Grade8'),
#                           (9, 'Grade9'), (10, 'Grade10'), (11, 'Grade11'), (12, 'Grade12'),
#                           )
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     student_number = models.CharField(max_length=12)
#     year_level = models.PositiveSmallIntegerField(choices=YEAR_LEVEL_CHOICES)
#     subjects = models.ManyToManyField(Subject)


# need to make a year level table para maging dynamic ang year level inputs
# mali din ang concept ko ng pag sign up sa students


class StudentProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                primary_key=True, related_name='user_studentprofile', limit_choices_to=Q(
                                    is_student=True))
    lrn = models.CharField(max_length=20)
    landline_number = models.CharField(max_length=11, null=True, blank=True)
    mobile_number = models.CharField(max_length=13, null=True, blank=True)
    address = models.TextField(max_length=300, blank=True)
    mothers_name = models.CharField(max_length=50)
    fathers_name = models.CharField(max_length=50)
    contact_person_name = models.CharField(max_length=50)
    contact_person_number = models.CharField(
        max_length=12, verbose_name='Phone number of Contact Person')
    class_advisor = models.ForeignKey(get_user_model(), limit_choices_to=Q(
        is_teacher=True), on_delete=models.SET_NULL, null=True, related_name='studentprofile_class_advisor')
    # class_advisor = models.OneToOneField(Teachers, on_delete=models.CASCADE)
    year = models.ForeignKey(YearLevel, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    class Meta:
        app_label = 'student_dashboard'
        db_table = 'accounts_studentprofile'  # <app_name>_<table_name>

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

# may mali dito regarding sa user level
@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        if not instance.is_student:
            StaffProfile.objects.create(user=instance)
            instance.user_staffprofile.save()
        elif instance.is_student:
            StudentProfile.objects.create(user=instance)
            instance.user_studentprofile.save()
