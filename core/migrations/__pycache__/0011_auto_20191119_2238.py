# Generated by Django 2.0.2 on 2019-11-19 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_semestres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
