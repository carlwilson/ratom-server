from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_CHOICES = (("ARCHIVIST", "Archivist"), ("RESEARCHER", "Researcher"))
    user_type = models.CharField(max_length=32, choices=USER_CHOICES)


class Collection(models.Model):
    title = models.CharField(max_length=200)
    accession_date = models.DateField(auto_now=False)

    def __str__(self) -> str:
        return str(self.title)


class Processor(models.Model):
    processed = models.BooleanField(default=False)
    is_record = models.BooleanField(default=True)
    has_pii = models.BooleanField(default=False)
    date_processed = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )


class Message(models.Model):
    message_id = models.CharField(max_length=256, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(db_index=True)
    msg_from = models.TextField(db_index=True)
    msg_to = models.TextField(db_index=True)
    msg_cc = models.TextField(blank=True)
    msg_bcc = models.TextField(blank=True)
    msg_subject = models.TextField(db_index=True)
    msg_body = models.TextField(blank=True)
    msg_tagged_body = models.TextField(blank=True)
    processor = models.OneToOneField(
        Processor, on_delete=models.PROTECT, null=True, blank=True
    )
