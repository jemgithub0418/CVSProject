from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def AdminHomeView(request):
    return render(request, template_name='admin_dashboard/admin_dashboard.html')
