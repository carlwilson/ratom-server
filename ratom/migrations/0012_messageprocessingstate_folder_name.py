# Generated by Django 2.2.7 on 2020-01-03 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratom', '0011_remove_messageprocessingstate_folder_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageprocessingstate',
            name='folder_name',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]