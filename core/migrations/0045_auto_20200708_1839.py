# Generated by Django 2.0.2 on 2020-07-08 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20200708_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrol',
            name='rol',
            field=models.TextField(null=True),
        ),
    ]