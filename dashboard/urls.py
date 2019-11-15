from django.urls import path
from dashboard import views as dashboard_views
urlpatterns = [
    path('registrar/', dashboard_views.RegistrarDashboardView, name='registrar-dashboard'),
    path('admin/', dashboard_views.AdminDashboardView, name='admin-dashboard'),
    path('teacher/', dashboard_views.TeacherDashboardView, name='teacher-dashboard'),
]
