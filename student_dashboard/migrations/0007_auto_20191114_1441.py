# Generated by Django 2.2.4 on 2019-11-14 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_dashboard', '0006_auto_20191114_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentgrade',
            name='period',
            field=models.CharField(choices=[('First Grading', 'First Grading'), ('Second Grading', 'Second Grading'), ('Third Grading', 'Third Grading'), ('Fourth Grading', 'Fourth Grading'), ('First Semester', 'First Semester'), ('Second Semester', 'Second Semester')], max_length=25),
        ),
    ]
