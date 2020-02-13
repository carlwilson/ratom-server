import pytest
from django.urls import reverse
from core.models import File

pytestmark = pytest.mark.django_db

# Account


def test_user_detail(api_client):
    url = reverse("user_detail")
    response = api_client.get(url)
    assert response.status_code == 200


def test_account_detail_account_exists(file_account, api_client):
    url = reverse("account_detail", args=[file_account.pk])
    response = api_client.get(url)
    assert response.status_code == 200


def test_account_detail_no_account(api_client):
    # Test No account exists
    url = reverse("account_detail", args=[5000])
    response = api_client.get(url)
    assert response.status_code == 404


def test_account_put_invalid(ratom_file, api_client):
    # Test PUT with invalid serializer
    url = reverse("account_detail", args=[ratom_file.account.pk])
    data = {"filename": "x" * 201}
    response = api_client.put(url, data=data)
    assert response.status_code == 400


def test_account_put_valid(ratom_file, api_client, celery_mock):
    # Test PUT with valid serializer
    url = reverse("account_detail", args=[ratom_file.account.pk])
    data = {"filename": ratom_file.filename}
    celery_mock.return_value = True
    response = api_client.put(url, data=data)
    assert response.status_code == 204


def test_account_delete(ratom_file, api_client):
    # Test Delete account
    url = reverse("account_detail", args=[ratom_file.account.pk])
    response = api_client.delete(url)
    assert response.status_code == 204


def test_account_list_get(file_account, api_client):
    url = reverse("account_list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]["title"] == file_account.title
    assert response.data[0]["files_in_account"] == 1
    assert response.data[0]["account_status"] == File.CREATED


def test_account_list_post_invalid_account(api_client):
    url = reverse("account_list")
    data = {"title": "x" * 201}
    response = api_client.post(url, data=data)
    assert response.status_code == 400


def test_account_list_post_invalid_file(api_client):
    url = reverse("account_list")
    data = {"title": "Good Title", "filename": "x" * 201}
    response = api_client.post(url, data=data)
    assert response.status_code == 400


def test_account_post_success(api_client, celery_mock):
    url = reverse("account_list")
    data = {"title": "Good Title", "filename": "Good Filename"}
    celery_mock.return_value = True
    response = api_client.post(url, data=data)
    assert response.status_code == 204


# File


def test_file_restart_file_ingest(ratom_file, api_client, celery_mock):
    ratom_file.import_status = File.FAILED
    ratom_file.save()
    url = reverse("restart_file")
    celery_mock.return_value = True
    response = api_client.post(url, data={"id": ratom_file.account.pk})
    assert response.status_code == 204


def test_file_restart_file_ingest_fail(ratom_file, api_client):
    # When no file has a FAILED status
    ratom_file.import_status = File.IMPORTING
    ratom_file.save()
    url = reverse("restart_file")
    response = api_client.post(url, data={"id": ratom_file.account.pk})
    assert response.status_code == 404
    # Should also return 404 if there is no account id
    response = api_client.post(url, data={"id": 600})
    assert response.status_code == 404
