# Generated by Django 4.2.9 on 2024-01-29 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_alter_student_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_name',
            field=models.CharField(default='', max_length=20),
        ),
    ]