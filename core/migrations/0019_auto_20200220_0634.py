# Generated by Django 2.0.2 on 2020-02-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20191217_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='archivo',
            field=models.FileField(default='settings.MEDIA_ROOT/prueba.jpg', upload_to='files/', verbose_name='Comentarios'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(default='hola', max_length=255, verbose_name='Estado'),
        ),
    ]
