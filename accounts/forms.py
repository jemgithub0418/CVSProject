from django import forms
from django.db import transaction
from accounts.models import (User, StaffProfile, StudentProfile)
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from phonenumber_field.formfields import PhoneNumberField


class StaffSignUpForm(UserCreationForm):
    user_level_choices = [('registrar', 'Registrar'), ('cm', 'Content Moderator'),
                          ('teacher', 'Teacher'), ('admin', 'Administrator'), ]
    email = forms.EmailField(
        max_length=254, help_text='Required. Please provide a valid email address.')
    user_level = forms.ChoiceField(
        label='Position', widget=forms.RadioSelect, choices=user_level_choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'middle_name', 'email', ]

    @transaction.atomic
    def save(self, commit=True):
        level = self.cleaned_data['user_level']
        user = super().save(commit=False)
        user.is_staff = True

        if level == 'registrar':
            user.is_registrar = True
        if level == 'cm':
            # user.is_content_moderator = True
            pass
        if level == 'teacher':
            user.is_teacher = True
        if level == 'admin':
            user.is_superuser = True

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['employee_number', 'mobile_number']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Please provide a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'middle_name',
                  'email', ]


class StaffProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['employee_number', 'mobile_number', 'address']


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['landline_number', 'mobile_number', 'address', 'mothers_name', 'fathers_name',
                  'contact_person_name', 'contact_person_number',
                  ]

    # class UserLoginForm(forms.Form):
    #     query = forms.CharField(label='Username')
    #     password = forms.CharField(label='Password', widget=forms.PasswordInput)
    #
    #     def clean(self, *args, **kwargs):
    #         query = self.cleaned_data.get('query')
    #         password = self.cleaned_data.get('password')
    #         user_qs_final = User.objects.filter(
    #             Q(username__iexact=query)
    #         ).distinct()
    #
    #         if not user_qs_final.exists() and user_qs_final.count != 1:
    #             raise forms.ValidationError('Invalid credentails.')
    #
    #         user_obj = user_qs_final.first()
    #         if not user_obj.check_password(password):
    #             raise forms.ValidationError('Invalid credentials')
    #         self.cleaned_data["user_obj"] = user_obj
    #         return super(UserLoginForm, self).clean(*args, **kwargs)
