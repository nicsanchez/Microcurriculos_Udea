# Generated by Django 2.0.2 on 2020-02-21 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20200221_2053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluation_2',
            options={'ordering': ['id'], 'verbose_name': 'Evaluacion', 'verbose_name_plural': 'Evaluaciones Editor'},
        ),
        migrations.AlterModelOptions(
            name='microcurriculum_2',
            options={'ordering': ['id'], 'verbose_name': 'Microcurriculo', 'verbose_name_plural': 'Microcurriculos Editor'},
        ),
        migrations.AlterModelOptions(
            name='unity_2',
            options={'ordering': ['id'], 'verbose_name': 'Unidad', 'verbose_name_plural': 'Unidades Editor'},
        ),
    ]
