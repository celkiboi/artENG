# Generated by Django 4.2.9 on 2024-01-29 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_alter_student_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_name',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
