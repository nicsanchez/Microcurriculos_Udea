# Generated by Django 2.0.2 on 2020-02-21 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20200220_0635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Versiones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.FileField(upload_to='versions/', verbose_name='Versiones')),
                ('accion', models.CharField(max_length=255, verbose_name='Accion')),
                ('comentarios', models.FileField(upload_to='files/', verbose_name='Comentarios')),
                ('usuario', models.CharField(max_length=255, verbose_name='Usuario que realizo la peticion')),
                ('coordinador', models.CharField(max_length=255, verbose_name='Coordinador que analizo la peticion')),
                ('id_microcurriculos', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Microcurriculum', verbose_name='Microcurriculo')),
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Versiones',
                'ordering': ['id'],
            },
        ),
    ]
