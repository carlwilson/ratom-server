# Generated by Django 2.2.10 on 2020-02-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200212_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmessageaudit',
            name='is_restricted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='messageaudit',
            name='is_restricted',
            field=models.BooleanField(default=False),
        ),
    ]