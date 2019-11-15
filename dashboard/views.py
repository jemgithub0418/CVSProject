from django.shortcuts import render, HttpResponse
from accounts.models import User
from django.contrib.auth.decorators import login_required


@login_required
def RegistrarDashboardView(request):
    return render(request, 'dashboard/registrar_dashboard.html', )


@login_required
def AdminDashboardView(request):

    return render(request, 'dashboard/admin_dashboard.html',)


@login_required
def TeacherDashboardView(request):

    return render(request, 'dashboard/teacher_dashboard.html',)
