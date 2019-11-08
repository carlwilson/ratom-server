# Generated by Django 2.2.7 on 2019-11-08 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='msg_body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='processor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ratom.Processor'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_date',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='processor',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
