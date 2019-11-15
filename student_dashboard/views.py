from django.shortcuts import render, get_object_or_404, get_list_or_404
from accounts.models import User, StudentProfile
from .models import StudentGrade
from django.db.models import Q
# Create your views here.


def StudentListView(request):
    sprofile = StudentProfile.objects.all()
    context = {
        'sprofile': sprofile,
    }
    return render(request, 'student_dashboard/student_list.html', context)


def StudentGradeView(request, id):
    student = get_list_or_404(StudentGrade, user_id=id)
    user = get_object_or_404(User, id=id)
    # studentname = f'{student.user.last_name}, {student.user.first_name}'
    # StudentGrade.objects.filter(user_id=id)
    context = {
        'student': student,
        'user': user,
    }
    return render(request, 'student_dashboard/student_grade.html', context)
