# Generated by Django 2.0.2 on 2019-12-17 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20191202_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='original',
            field=models.CharField(default='', max_length=255, verbose_name='Microcurriculo Original'),
        ),
    ]