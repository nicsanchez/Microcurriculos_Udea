# Generated by Django 2.0.2 on 2020-04-27 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20200327_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='vigencias_original',
            field=models.CharField(max_length=255, null=True, verbose_name='Vigencia Original'),
        ),
    ]