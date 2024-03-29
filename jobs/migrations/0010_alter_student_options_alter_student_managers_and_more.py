# Generated by Django 4.2.9 on 2024-01-29 19:04

from django.db import migrations, models
import django.utils.timezone
import jobs.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_remove_student_name_remove_student_surname_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterModelManagers(
            name='student',
            managers=[
                ('objects', jobs.models.CustomStudentManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='username',
        ),
        migrations.AddField(
            model_name='student',
            name='user_name',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
    ]
