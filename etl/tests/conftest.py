import datetime as dt
import pytest
from unittest import mock
from email.message import EmailMessage


from libratom.lib.pff import PffArchive

from etl.importer import PstImporter
from etl.providers.factory import import_provider_factory, ProviderTypes

headers = [
    "date: Mon, 2 Apr 2001 11:10:00 -0700 (PDT) Mon, 2 Apr 2001 11:10:00 -0700  (PDT)",
    "Message-ID: <PPCBV2QFM1HWPI3I1YTQ5013JUTHIZOCB@zlsvr22>",
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="us-ascii"',
    "Content-Transfer-Encoding: 7bit",
    'from: "Lester Rawson"',
    'to: "Kate Symes"',
    "subject: Re: Unit Contingent Deals",
    "filename: kate symes 6-27-02.nsf",
    "folder: \\kate symes 6-27-02\\Notes Folders\\All documents",
]

bad_header = [
    "Bad Header No Colon",
]


@pytest.fixture()
def local_file(tmp_path):
    """Basic tempfile on filesystem"""
    sub_directory = tmp_path / "sub"
    sub_directory.mkdir()
    pst_file = sub_directory / "name.pst"
    pst_file.write_text("CONTENT")
    import_provider = import_provider_factory(provider=ProviderTypes.FILESYSTEM)
    yield import_provider(file_path=str(pst_file.absolute()))


@pytest.fixture
def empty_message():
    """
    Returns:
        A mock message with empty components
    """

    message = mock.Mock()
    for attr in ("plain_text_body", "html_body", "rtf_body", "transport_headers"):
        setattr(message, attr, "")

    yield message


@pytest.fixture
def archive_msg(empty_message):
    """A mock pypff message with fake data."""
    empty_message.delivery_time = dt.datetime(2020, 1, 1)
    empty_message.identifier = 2097220
    empty_message.plain_text_body = "Hello, World!"
    empty_message.transport_headers = "\r\n".join(headers)
    yield empty_message


@pytest.fixture
def archive_folder(archive_msg):
    """A mock pypff folder with archive_msg in it."""
    folder = mock.Mock()
    folder.name = "Inbox"
    folder.get_number_of_sub_messages.return_value = 1
    folder.sub_messages = mock.Mock()
    folder.sub_messages = [archive_msg]
    yield folder


@pytest.fixture
def email_message(archive_msg):
    em = EmailMessage()
    em.set_payload(archive_msg.plain_text_body)
    for i in headers:
        s = i.split(":", maxsplit=1)
        em[s[0]] = s[1]
    yield em


@pytest.fixture
def email_message_w_bad_header(archive_msg):
    em = EmailMessage()
    em.set_payload(archive_msg.plain_text_body)
    for i in headers:
        s = i.split(":", maxsplit=1)
        em[s[0]] = s[1]
    em[bad_header[0]] = ""
    yield em


@pytest.fixture()
def test_archive(archive_folder):
    """A mock pypff archive with ."""
    with mock.patch("etl.providers.base.PffArchive") as _mock:
        archive = _mock.return_value
        archive.message_count = 1
        archive.folders.return_value = [archive_folder]
        archive.format_message = mock.MagicMock(side_effect=PffArchive.format_message)
        yield _mock


@pytest.fixture()
def pst_importer(account, local_file, test_archive):
    """PstImporter instance"""
    importer = PstImporter(local_file, account, mock.MagicMock())
    importer.get_folder_abs_path = mock.MagicMock(return_value="/Important/Project/")
    yield importer


@pytest.fixture
def html_file():
    """
    A mock html file to test scrubbing features
    """
    html = """
    <html><head></head><body>
    <p>I am a paragraph. I have an image
    <img src="http://example.com/images/img0001.png" width="10" height="10" alt="test image">
    </p>

    <p>I'm fine</p>
    <script>I am bad</script>

    </body></html>
    """
    yield html
