import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_list_archive_notes(admin_client):
    response = list_archive_notes(admin_client)

    assert response.status_code == HTTP_200_OK


def test_admin_user_can_retrieve_archive_note(admin_client, archive_note):
    response = retrieve_archive_note(admin_client, archive_note)

    assert response.status_code == HTTP_200_OK


def test_user_cannot_list_archive_notes(client):
    response = list_archive_notes(client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_cannot_retrieve_archive_note(client, archive_note):
    response = retrieve_archive_note(client, archive_note)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_list_archive_notes(anonymous_client):
    response = list_archive_notes(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_retrieve_archive_notes(anonymous_client, archive_note):
    response = retrieve_archive_note(anonymous_client, archive_note)

    assert response.status_code == HTTP_403_FORBIDDEN


def list_archive_notes(client):
    return client.get(reverse('archivenote-list'))


def retrieve_archive_note(client, archive_note):
    return client.get(reverse('archivenote-detail', kwargs=dict(pk=archive_note.pk)))
