import pytest

from django.urls import reverse
from django_elasticsearch_dsl.registries import registry

from api.documents.message import MessageDocument
from core.tests import factories


@pytest.fixture(scope="function", autouse=True)
def elasticsearch(request):
    registry.register_document(MessageDocument)

    def delete_indices():
        for index in registry.get_indices():
            index.delete(ignore=404)

    delete_indices()
    for index in registry.get_indices():
        index.create()
    # always clean up indicies at end of scoped context
    request.addfinalizer(delete_indices)


@pytest.fixture
def url():
    return reverse("search_messages")


@pytest.fixture
def export_url():
    return reverse("export_messages")


@pytest.fixture
def account_eric():
    return factories.AccountFactory()


@pytest.fixture
def account_sally():
    return factories.AccountFactory()


@pytest.fixture
def file_eric(account_eric):
    return factories.FileFactory(account=account_eric)


@pytest.fixture
def file_sally(account_sally):
    return factories.FileFactory(account=account_sally)


@pytest.fixture
def eric1(file_eric):
    return factories.MessageFactory(account=file_eric.account, file=file_eric)


@pytest.fixture
def sally1(file_sally):
    return factories.MessageFactory(account=file_sally.account, file=file_sally)


@pytest.fixture
def sally2(file_sally):
    return factories.MessageFactory(account=file_sally.account, file=file_sally)


@pytest.fixture
def sally3(file_sally):
    return factories.MessageFactory(account=file_sally.account, file=file_sally)


@pytest.fixture
def sally4_known_bodies(file_sally, sally1, sally2, sally3):
    message1 = factories.MessageFactory(account=file_sally.account, file=file_sally)
    message1.body += " FileZilla"
    message1.save()
    message2 = factories.MessageFactory(account=file_sally.account, file=file_sally)
    message2.subject += " Zombie"
    message2.save()
    return message1, message2


@pytest.fixture
def event():
    return factories.LabelFactory(name="EVENT")


@pytest.fixture
def org():
    return factories.LabelFactory(name="ORG")


@pytest.fixture
def date():
    return factories.LabelFactory(name="DATE")
