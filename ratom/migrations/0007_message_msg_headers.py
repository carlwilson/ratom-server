# Generated by Django 2.2.7 on 2019-11-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ratom", "0006_auto_20191117_1059"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="msg_headers",
            field=models.TextField(blank=True),
        ),
    ]
