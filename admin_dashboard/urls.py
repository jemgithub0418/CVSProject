from django.urls import path
from admin_dashboard import views as admin_dashboard_views

urlpatterns = [
    path('admin/', admin_dashboard_views.AdminHomeView, name='admin-dashboard')
]
