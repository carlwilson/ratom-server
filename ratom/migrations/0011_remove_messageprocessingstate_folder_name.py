# Generated by Django 2.2.7 on 2020-01-03 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratom', '0010_messageprocessingstate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageprocessingstate',
            name='folder_name',
        ),
    ]