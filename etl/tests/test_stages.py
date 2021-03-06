from pathlib import Path
import pytest
from unittest import mock

from core import models as ratom

pytestmark = pytest.mark.django_db


def test_create_ratom_file(pst_importer, local_file, account):
    """Importer should create ratom.File with correct initial values."""
    ratom_file = pst_importer._create_ratom_file(account, local_file)
    assert str(local_file.path) == ratom_file.original_path
    assert str(local_file.file_name) == ratom_file.filename


def test_create_ratom_file__missing(pst_importer, account, local_file):
    """Importer shouldn't fail with non-existent file."""
    local_file.local_path = Path("i-dont-exist.pst")
    ratom_file = pst_importer._create_ratom_file(account, local_file)
    pst_importer.initializing_stage()
    assert not ratom_file.file_size


def test_get_sha256_before_open_fails(pst_importer, account, local_file):
    pst_importer._create_ratom_file(account, local_file)
    pst_importer.initializing_stage()
    with pytest.raises(AssertionError):
        assert pst_importer.ratom_file.sha256


def test_get_sha256_after_open_succeeds(pst_importer, account, local_file):
    pst_importer._create_ratom_file(account, local_file)
    pst_importer.initializing_stage()
    pst_importer.importing_stage()
    assert pst_importer.ratom_file.sha256


@pytest.mark.parametrize("message_count", [100, 1_000])
def test_importing_stage_message_count(test_archive, pst_importer, message_count):
    """Acrhive's reported total messages is saved to model"""
    test_archive.return_value.message_count = message_count
    pst_importer.initializing_stage()
    pst_importer.importing_stage()
    assert ratom.File.objects.count() == 1
    ratom_file = pst_importer.ratom_file
    ratom_file.refresh_from_db()
    assert ratom_file.reported_total_messages == message_count


def test_add_file_error__no_msg(pst_importer):
    """File-level errors are added to internal list."""
    name = "Error Name"
    context = {"key": "value"}
    pst_importer.add_file_error(name, context)
    assert len(pst_importer.ratom_file_errors) == 1
    assert pst_importer.ratom_file_errors[0]["name"] == name
    assert pst_importer.ratom_file_errors[0]["context"] == context


def test_sent_date__errors(pst_importer, email_message):
    """sent_date errors should be saved to message object."""
    with mock.patch("etl.message.forms.make_aware", side_effect=Exception):
        pst_importer.run()
        m = ratom.Message.objects.get()
        assert m.errors


class TestFileErrors:
    def test_add_file_error__with_msg(self, pst_importer, archive_msg):
        """Message identifier included in file level error."""
        name = "Error Name"
        context = {"key": "value"}
        pst_importer.add_file_error(name, context, archive_msg)
        assert (
            pst_importer.ratom_file_errors[0]["msg_identifier"]
            == archive_msg.identifier
        )

    def test_create_message__captures_error(self, pst_importer):
        """If create_message() fails, an error should be added to ratom_file_errors."""
        pst_importer.create_message = mock.MagicMock(side_effect=Exception)
        pst_importer.run()
        assert len(pst_importer.ratom_file_errors) == 1
        assert pst_importer.ratom_file_errors[0]["name"] == "create_message() failed"

    def test_import_failure(self, pst_importer):
        """Uncrecoverable errors should log to the DB."""
        pst_importer.importing_stage = mock.MagicMock(side_effect=Exception)
        pst_importer.run()
        ratom_file = ratom.File.objects.get()
        assert ratom_file.import_status == ratom.File.FAILED
        errors = ratom_file.errors
        assert len(errors) == 1
        assert errors[0]["name"] == "Unrecoverable import error"

    def test_import_success__message_failure(self, pst_importer, archive_msg):
        """Failed message errors should still be saved to DB."""
        type(archive_msg).transport_headers = mock.PropertyMock(side_effect=Exception)
        pst_importer.run()
        ratom_file = ratom.File.objects.get()
        assert ratom_file.import_status == ratom.File.COMPLETE
        assert "create_message() failed" in ratom_file.errors[0]["name"]
