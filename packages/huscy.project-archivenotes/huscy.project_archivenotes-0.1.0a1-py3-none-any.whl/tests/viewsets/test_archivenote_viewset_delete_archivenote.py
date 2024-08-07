import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_archive_note(admin_client, archive_note):
    response = delete_archive_note(admin_client, archive_note)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_cannot_delete_archive_note(client, archive_note):
    response = delete_archive_note(client, archive_note)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_delete_archive_note(anonymous_client, archive_note):
    response = delete_archive_note(anonymous_client, archive_note)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_archive_note(client, archive_note):
    return client.delete(reverse('archivenote-detail', kwargs=dict(pk=archive_note.pk)))
