# Generated by Django 4.2.9 on 2024-01-29 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_alter_student_email_alter_student_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='surname',
        ),
    ]
