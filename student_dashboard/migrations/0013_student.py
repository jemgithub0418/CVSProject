# Generated by Django 2.2.4 on 2021-08-13 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_dashboard', '0012_delete_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_dashboard.Subject')),
                ('student', models.ForeignKey(limit_choices_to=models.Q(is_student=True), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
