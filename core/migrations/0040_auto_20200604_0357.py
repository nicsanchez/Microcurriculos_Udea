# Generated by Django 2.0.2 on 2020-06-04 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20200603_0311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userrol',
            options={'ordering': ['id'], 'verbose_name': 'Atributo', 'verbose_name_plural': 'Atributos'},
        ),
    ]