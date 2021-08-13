from django import forms
from accounts.models import User
from student_dashboard.models import Student

class AddStudentGradeForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     super(AddStudentGradeForm, self).__init__(*args, **kwargs)
    #     self.initial['student'] = (None,'------')

    student_list = Student.objects.all().prefetch_related('enrolled_subject')

    student_choices = [(None,'-----')]
    enrolled_subjects = []

    for  student in student_list:
        full_name = student.student.first_name + " " + student.student.last_name
        student_choices.append((student.student.id, full_name))
        for subject in student.enrolled_subject.all():
            enrolled_subjects.append((subject.id,subject.subject_name))



    student = forms.ChoiceField(widget= forms.Select, choices= student_choices,initial=None)
    subject = forms.ChoiceField(widget= forms.Select, choices= enrolled_subjects)
