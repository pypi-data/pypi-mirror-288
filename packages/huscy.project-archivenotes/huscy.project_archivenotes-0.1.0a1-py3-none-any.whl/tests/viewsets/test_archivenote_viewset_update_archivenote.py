import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.project_archivenotes.models import ArchiveNote

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_archive_note(admin_client, archive_note):
    response = update_archive_note(admin_client, archive_note)

    assert response.status_code == HTTP_200_OK


def test_user_cannot_update_archive_note(client, archive_note):
    response = update_archive_note(client, archive_note)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_update_archive_note(anonymous_client, archive_note):
    response = update_archive_note(anonymous_client, archive_note)

    assert response.status_code == HTTP_403_FORBIDDEN


def update_archive_note(client, archive_note):
    data = dict(
        action=ArchiveNote.ACTIONS.get_value('retrieve'),
        note='note',
        depositor=archive_note.depositor.pk,
        depositor_name=archive_note.depositor.username,
        project=archive_note.project.pk,
    )
    return client.put(reverse('archivenote-detail', kwargs=dict(pk=archive_note.pk)), data=data)
