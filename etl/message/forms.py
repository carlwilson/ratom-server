import logging
import pytz
import re
from typing import Dict, List, Any

from django import forms
from django.utils.timezone import make_aware

from core.models import Message, MessageAudit
from etl.message.headers import MessageHeader


logger = logging.getLogger(__name__)


def clean_null_chars(obj: str) -> str:
    """Cleans strings of postgres breaking null chars.

    Arguments:
        obj {str}

    Returns:
        str
    """
    return re.sub("\x00", "", obj)


class ArchiveMessageForm(forms.ModelForm):

    # we manually clean sent_date in clean_sent_date() below
    # so just define as a CharField here
    sent_date = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.archive = kwargs.pop("archive")
        self.archive_msg = kwargs.pop("archive_msg")
        msg_data = self._prepare_message()
        kwargs["data"] = msg_data
        super().__init__(*args, **kwargs)
        # Remove ProhibitNullCharactersValidator since we want to
        # remove them in clean rather than returning invalid
        self.fields["body"].validators = []
        self.msg_errors = []

    def _prepare_message(self) -> Dict[str, str]:
        """Prepare message for Form-based validation."""
        msg_data = {}
        try:
            headers = MessageHeader(self.archive_msg.transport_headers)
        except AttributeError as e:
            logger.exception(f"{e}")
            raise
        msg_data.update(
            {
                "source_id": self.archive_msg.identifier,
                "msg_from": headers.get_header("From"),
                "msg_to": headers.get_header("To"),
                "msg_cc": headers.get_header("Cc"),
                "msg_bcc": headers.get_header("Bcc"),
                "subject": headers.get_header("Subject"),
                "headers": headers.get_full_headers(),
                "body": self.archive.format_message(
                    self.archive_msg, with_headers=False
                ),
            }
        )
        return msg_data

    def clean_sent_date(self):
        """If parsing sent_date fails, record error and move on."""
        sent_date = self.archive_msg.delivery_time
        try:
            sent_date = make_aware(sent_date)
        except Exception as e:
            logger.warning(f"{repr(e)} [msg.identifier=={self.archive_msg.identifier}]")
            self.msg_errors.append(("sent_date", e.__class__.__name__, str(e)))
            sent_date = None
        return sent_date

    def clean_body(self):
        return clean_null_chars(self.cleaned_data["body"])

    class Meta:
        model = Message
        fields = [
            "source_id",
            "sent_date",
            "msg_from",
            "msg_to",
            "msg_cc",
            "msg_bcc",
            "subject",
            "body",
            "directory",
            "headers",
        ]