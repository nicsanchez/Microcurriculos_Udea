# Generated by Django 2.0.2 on 2020-03-27 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20200327_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versiones',
            name='id_microcurriculos_2',
            field=models.ForeignKey(null=True, on_delete='', to='core.Microcurriculum_2', verbose_name='Microcurriculo fantasma'),
        ),
    ]
