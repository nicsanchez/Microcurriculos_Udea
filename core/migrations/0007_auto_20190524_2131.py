# Generated by Django 2.0.2 on 2019-05-24 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190514_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microcurriculum',
            name='vigencia',
        ),
        migrations.AddField(
            model_name='microcurriculum',
            name='desde',
            field=models.CharField(default='', max_length=255, verbose_name='Desde'),
        ),
        migrations.AddField(
            model_name='microcurriculum',
            name='hasta',
            field=models.CharField(default='', max_length=255, verbose_name='Hasta'),
        ),
        migrations.AlterField(
            model_name='programa',
            name='nombre_progr',
            field=models.CharField(max_length=255, verbose_name='Nombre del programa'),
        ),
    ]
