# Generated by Django 2.0.2 on 2020-06-16 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20200604_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrol',
            name='cursos',
        ),
        migrations.AddField(
            model_name='userrol',
            name='cursos',
            field=models.ManyToManyField(to='core.Curso_asignado', verbose_name='Cursos'),
        ),
    ]
