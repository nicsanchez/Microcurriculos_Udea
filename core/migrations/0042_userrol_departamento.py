# Generated by Django 2.0.2 on 2020-07-08 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20200616_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrol',
            name='departamento',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Programa'),
        ),
    ]