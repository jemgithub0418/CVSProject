# Generated by Django 2.2.4 on 2021-08-12 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ['-date_posted']},
        ),
    ]
