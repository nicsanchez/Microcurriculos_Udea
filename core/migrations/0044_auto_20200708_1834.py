# Generated by Django 2.0.2 on 2020-07-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20200708_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrol',
            name='cursos',
            field=models.ManyToManyField(to='core.Curso_asignado', verbose_name='Cursos'),
        ),
    ]
