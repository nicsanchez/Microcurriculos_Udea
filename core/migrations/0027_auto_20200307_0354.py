# Generated by Django 2.0.2 on 2020-03-07 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200221_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versiones',
            name='id_microcurriculos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Microcurriculum', verbose_name='Microcurriculo final'),
        ),
    ]
