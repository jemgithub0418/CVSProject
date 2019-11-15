from django.urls import path
from student_dashboard import views as stud_dash_view

urlpatterns = [
    path('', stud_dash_view.StudentListView, name='student-list'),
    path('grade/<int:id>/', stud_dash_view.StudentGradeView, name='student-grade'),

]
