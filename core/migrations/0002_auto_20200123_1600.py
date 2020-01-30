# Generated by Django 2.2.8 on 2020-01-23 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='type',
            field=models.CharField(choices=[('U', 'User'), ('I', 'Importer'), ('S', 'Static')], max_length=1),
        ),
    ]