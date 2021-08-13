# these are action flags from the docs
from django.contrib.admin.utils import construct_change_message
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from accounts.models import User, StaffProfile
from accounts import forms as accounts_forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
from verseoftheday.models import VerseOfTheDay
from announcement.models import Announcement
User = get_user_model()
from admin_dashboard.forms import AddStudentGradeForm
from student_dashboard.models import Student, Subject, StudentGrade

def home(request):
    verses = VerseOfTheDay.objects.all()
    news = Announcement.objects.all()
    student_grade_form = AddStudentGradeForm()
    students = Student.objects.all().prefetch_related('enrolled_subject')
    context = {
        "verse": verses,
        'news': news,
        'form': student_grade_form,
        'students': students,

    }

    if request.method == "POST":
        data = request.POST
        grade_list = data.getlist('grade')
        print(grade_list)
        subject_list = data.getlist('subject')
        print(subject_list)

        student = User.objects.get(pk= data.get('studentid'))
        print(data.get('studentid'))

        i=0
        while i < len(grade_list):
            enrolled_subject = Subject.objects.get(pk= subject_list[i])
            new_grade = StudentGrade(user= student, period= data.get('period'), subject= enrolled_subject, grade=grade_list[i])
            new_grade.save()
            i+= 1




    return render(request, 'home.html', context)


@login_required
def StaffSignUpView(request):
    if request.method == 'POST':
        userform = accounts_forms.StaffSignUpForm(request.POST)
        profileform = accounts_forms.UserProfileForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            userprofile = profileform.save(commit=False)
            userprofile.user = user
            userprofile.save()
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name')
            message = f'New user added. Added staff profile for {user.first_name} {user.last_name}.'

            log = LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(user).pk,
                object_id=str(user.id),
                object_repr=str(user.username),
                action_flag=ADDITION,
                # change_message=message,

            )
            log.save()

            # log_addition()

            messages.success(request, 'Account created for {0} {1}!'.format(
                first_name, last_name))
            return redirect('home')
    else:
        userform = accounts_forms.StaffSignUpForm()
        profileform = accounts_forms.UserProfileForm()

    context = {
        'profileform': profileform,
        'form': userform,
    }

    return render(request, 'accounts/registration/register.html', context)


@login_required
def ProfileUpdateView(request):
    try:
        if request.method == 'POST':
            user_form = accounts_forms.UserUpdateForm(request.POST, instance=request.user)
            if request.user.is_staff == True:
                profile_form = accounts_forms.StaffProfileUpdateForm(
                    request.POST, instance=request.user.user_staffprofile)
                # pag may picture ung form kailangan ata mag add ng request.FIle
            else:
                profile_form = accounts_forms.StudentProfileUpdateForm(
                    request.POST, instance=request.user.user_studentprofile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                messages.success(request, 'Your profile has been updated.')
                return redirect('update-profile')
            else:
                print('king ina hindi valid')
                print(request.user.user_studentprofile.lrn)

        else:
            user_form = accounts_forms.UserUpdateForm(instance=request.user)
            if request.user.is_staff == True:
                profile_form = accounts_forms.StaffProfileUpdateForm(
                    instance=request.user.user_staffprofile)
            else:
                profile_form = accounts_forms.StudentProfileUpdateForm(
                    instance=request.user.user_studentprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    return render(request, 'accounts/update_profile.html', context)
