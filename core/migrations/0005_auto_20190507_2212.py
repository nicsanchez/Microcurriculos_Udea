# Generated by Django 2.0.2 on 2019-05-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190507_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='microcurriculum',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='unity',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
